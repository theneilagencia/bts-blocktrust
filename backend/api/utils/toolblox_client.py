"""
Cliente robusto para integração com Toolblox API
Inclui retry logic, logging e sistema de alertas
"""
import os
import time
import logging
import requests
from datetime import datetime
from typing import Dict, Any, Optional
import socket

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Variáveis de ambiente
TOOLBLOX_MINT_URL = os.getenv('TOOLBLOX_MINT_IDENTITY_URL')
TOOLBLOX_SIGNATURE_URL = os.getenv('TOOLBLOX_REGISTER_SIGNATURE_URL')
TOOLBLOX_VERIFY_URL = os.getenv('TOOLBLOX_VERIFY_URL')
TOOLBLOX_NETWORK = os.getenv('TOOLBLOX_NETWORK', 'amoy')
WEBHOOK_URL = os.getenv('ALERT_WEBHOOK_URL')  # Discord/Slack webhook para alertas

# Configurações de retry
MAX_RETRIES = 3
INITIAL_BACKOFF = 2  # segundos
TIMEOUT = 60  # segundos


class ToolbloxError(Exception):
    """Exceção customizada para erros do Toolblox"""
    pass


class ToolbloxClient:
    """Cliente para integração com Toolblox API"""
    
    def __init__(self):
        # Aplicar fallback para URLs com domínio antigo
        self.mint_url = self._fix_url(TOOLBLOX_MINT_URL)
        self.signature_url = self._fix_url(TOOLBLOX_SIGNATURE_URL)
        self.verify_url = self._fix_url(TOOLBLOX_VERIFY_URL)
        self.network = TOOLBLOX_NETWORK or 'polygon'
        self.webhook_url = WEBHOOK_URL
        
        # Validar configurações
        self._validate_config()
    
    def _fix_url(self, url: Optional[str]) -> Optional[str]:
        """Corrige URLs com domínio antigo run.toolblox.net para api.toolblox.net"""
        if not url:
            return url
        
        # Substituir run.toolblox.net por api.toolblox.net/run
        if 'run.toolblox.net' in url:
            url = url.replace('run.toolblox.net', 'api.toolblox.net/run')
            logger.info(f"✅ URL corrigida: {url}")
        
        return url
    
    def _validate_config(self):
        """Valida se as URLs estão configuradas corretamente"""
        if not self.mint_url:
            logger.warning("TOOLBLOX_MINT_IDENTITY_URL não configurada")
        if not self.signature_url:
            logger.warning("TOOLBLOX_REGISTER_SIGNATURE_URL não configurada")
        if not self.verify_url:
            logger.warning("TOOLBLOX_VERIFY_URL não configurada")
        
        # Validar DNS para cada URL configurada
        for name, url in [
            ('MINT', self.mint_url),
            ('SIGNATURE', self.signature_url),
            ('VERIFY', self.verify_url)
        ]:
            if url:
                self._validate_dns(name, url)
    
    def _validate_dns(self, name: str, url: str):
        """Valida se o DNS do endpoint é resolvível"""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            hostname = parsed.hostname
            
            if hostname:
                socket.gethostbyname(hostname)
                logger.info(f"✅ DNS resolvido para {name}: {hostname}")
        except socket.gaierror as e:
            logger.error(f"❌ Erro de DNS para {name} ({url}): {e}")
            self._send_alert(f"Erro de DNS para endpoint {name}", str(e))
    
    def _send_alert(self, title: str, message: str):
        """Envia alerta via webhook (Discord/Slack)"""
        if not self.webhook_url:
            logger.warning("ALERT_WEBHOOK_URL não configurada, alerta não enviado")
            return
        
        try:
            payload = {
                "content": f"🚨 **{title}**\n```\n{message}\n```\nTimestamp: {datetime.now().isoformat()}"
            }
            
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=10
            )
            
            if response.status_code in [200, 204]:
                logger.info("✅ Alerta enviado com sucesso")
            else:
                logger.error(f"❌ Falha ao enviar alerta: {response.status_code}")
        except Exception as e:
            logger.error(f"❌ Erro ao enviar alerta: {e}")
    
    def _make_request_with_retry(
        self,
        url: str,
        payload: Dict[str, Any],
        endpoint_name: str
    ) -> Dict[str, Any]:
        """
        Faz requisição HTTP com retry logic e backoff exponencial
        
        Args:
            url: URL do endpoint
            payload: Dados a serem enviados
            endpoint_name: Nome do endpoint para logging
        
        Returns:
            Resposta JSON do endpoint
        
        Raises:
            ToolbloxError: Se todas as tentativas falharem
        """
        if not url:
            error_msg = f"URL não configurada para {endpoint_name}"
            logger.error(error_msg)
            raise ToolbloxError(error_msg)
        
        last_exception = None
        
        for attempt in range(1, MAX_RETRIES + 1):
            backoff_time = INITIAL_BACKOFF * (2 ** (attempt - 1))
            
            try:
                logger.info(
                    f"🔄 Tentativa {attempt}/{MAX_RETRIES} para {endpoint_name}\n"
                    f"   URL: {url}\n"
                    f"   Payload: {payload}"
                )
                
                response = requests.post(
                    url,
                    json=payload,
                    timeout=TIMEOUT,
                    headers={'Content-Type': 'application/json'}
                )
                
                # Log da resposta
                logger.info(
                    f"📥 Resposta de {endpoint_name}:\n"
                    f"   Status: {response.status_code}\n"
                    f"   Body: {response.text[:500]}"
                )
                
                # Se sucesso, retornar
                if response.status_code == 200:
                    logger.info(f"✅ Sucesso em {endpoint_name} na tentativa {attempt}")
                    return response.json()
                
                # Se erro 4xx, não tentar novamente
                if 400 <= response.status_code < 500:
                    error_msg = f"Erro {response.status_code} em {endpoint_name}: {response.text}"
                    logger.error(error_msg)
                    raise ToolbloxError(error_msg)
                
                # Se erro 5xx, tentar novamente
                logger.warning(
                    f"⚠️ Erro {response.status_code} em {endpoint_name}, "
                    f"tentando novamente em {backoff_time}s..."
                )
                
            except requests.exceptions.Timeout as e:
                last_exception = e
                logger.warning(
                    f"⏱️ Timeout em {endpoint_name} (tentativa {attempt}/{MAX_RETRIES}), "
                    f"tentando novamente em {backoff_time}s..."
                )
            
            except requests.exceptions.ConnectionError as e:
                last_exception = e
                logger.warning(
                    f"🔌 Erro de conexão em {endpoint_name} (tentativa {attempt}/{MAX_RETRIES}), "
                    f"tentando novamente em {backoff_time}s..."
                )
            
            except requests.exceptions.RequestException as e:
                last_exception = e
                logger.warning(
                    f"❌ Erro de requisição em {endpoint_name} (tentativa {attempt}/{MAX_RETRIES}): {e}, "
                    f"tentando novamente em {backoff_time}s..."
                )
            
            # Se não for a última tentativa, aguardar backoff
            if attempt < MAX_RETRIES:
                time.sleep(backoff_time)
        
        # Se chegou aqui, todas as tentativas falharam
        error_msg = (
            f"❌ Todas as {MAX_RETRIES} tentativas falharam para {endpoint_name}\n"
            f"Último erro: {last_exception}"
        )
        logger.error(error_msg)
        self._send_alert(f"Falha em {endpoint_name}", error_msg)
        raise ToolbloxError(error_msg)
    
    def mint_identity(self, wallet: str, proof_cid: str) -> Dict[str, Any]:
        """
        Mint de identidade via Toolblox
        
        Args:
            wallet: Endereço da carteira
            proof_cid: CID do proof no IPFS
        
        Returns:
            Resposta do Toolblox com token_id
        """
        payload = {
            'wallet': wallet,
            'proof_cid': proof_cid,
            'network': self.network
        }
        
        return self._make_request_with_retry(
            self.mint_url,
            payload,
            'MINT_IDENTITY'
        )
    
    def register_signature(self, doc_hash: str, signer: str) -> Dict[str, Any]:
        """
        Registra assinatura de documento via Toolblox
        
        Args:
            doc_hash: Hash do documento
            signer: Endereço do assinante
        
        Returns:
            Resposta do Toolblox com tx_hash
        """
        payload = {
            'hash': doc_hash,
            'signer': signer,
            'network': self.network
        }
        
        return self._make_request_with_retry(
            self.signature_url,
            payload,
            'REGISTER_SIGNATURE'
        )
    
    def verify_document(self, doc_hash: str) -> Dict[str, Any]:
        """
        Verifica documento via Toolblox
        
        Args:
            doc_hash: Hash do documento
        
        Returns:
            Resposta do Toolblox com status de verificação
        """
        payload = {
            'hash': doc_hash,
            'network': self.network
        }
        
        return self._make_request_with_retry(
            self.verify_url,
            payload,
            'VERIFY_DOCUMENT'
        )


# Instância global do cliente
toolblox_client = ToolbloxClient()

