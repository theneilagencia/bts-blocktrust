"""
Integração com Sumsub para KYC e Liveness Check
"""
import os
import requests
import time
import hmac
import hashlib
import json
import logging

logger = logging.getLogger(__name__)

SUMSUB_APP_TOKEN = os.getenv('SUMSUB_APP_TOKEN')
SUMSUB_SECRET_KEY = os.getenv('SUMSUB_SECRET_KEY')
SUMSUB_WEBHOOK_SECRET = os.getenv('SUMSUB_WEBHOOK_SECRET', SUMSUB_SECRET_KEY)
SUMSUB_BASE_URL = 'https://api.sumsub.com'
SUMSUB_LEVEL_NAME = os.getenv('SUMSUB_LEVEL_NAME', 'basic-kyc-level')

def validate_credentials():
    """
    Valida se as credenciais do Sumsub estão configuradas
    
    Returns:
        Tuple (bool, str): (is_valid, error_message)
    """
    if not SUMSUB_APP_TOKEN:
        return False, "SUMSUB_APP_TOKEN não configurado"
    if not SUMSUB_SECRET_KEY:
        return False, "SUMSUB_SECRET_KEY não configurado"
    return True, None

def retry_request(func, max_retries=3, delays=[2, 4, 8]):
    """
    Executa uma função com retry e backoff exponencial
    
    Args:
        func: Função a ser executada
        max_retries: Número máximo de tentativas
        delays: Lista de delays entre tentativas (em segundos)
    
    Returns:
        Resultado da função ou None em caso de falha
    """
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            logger.error(f"Tentativa {attempt + 1}/{max_retries} falhou: {str(e)}")
            if attempt < max_retries - 1:
                delay = delays[attempt] if attempt < len(delays) else delays[-1]
                logger.info(f"Aguardando {delay}s antes da próxima tentativa...")
                time.sleep(delay)
            else:
                logger.error(f"Todas as {max_retries} tentativas falharam")
                raise

def generate_signature(method, url, body='', ts=None):
    """
    Gera assinatura HMAC SHA256 para requisições Sumsub
    
    Args:
        method: Método HTTP (GET, POST, etc.)
        url: URL do endpoint (path relativo)
        body: Corpo da requisição (opcional)
        ts: Timestamp (opcional, gerado automaticamente se não fornecido)
    
    Returns:
        Tupla (timestamp, signature)
    """
    if not SUMSUB_SECRET_KEY:
        raise ValueError("SUMSUB_SECRET_KEY não configurado")
    
    if ts is None:
        ts = str(int(time.time()))
    
    # Converte body para string se for dict
    if isinstance(body, dict):
        body = json.dumps(body)
    
    signature_string = f'{ts}{method.upper()}{url}{body}'
    
    signature = hmac.new(
        SUMSUB_SECRET_KEY.encode('utf-8'),
        signature_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    return ts, signature

def get_headers(method, url, body=''):
    """
    Gera headers para requisições Sumsub
    
    Args:
        method: Método HTTP
        url: URL do endpoint
        body: Corpo da requisição (opcional)
    
    Returns:
        Dict com headers necessários
    """
    if not SUMSUB_APP_TOKEN:
        raise ValueError("SUMSUB_APP_TOKEN não configurado")
    
    ts, signature = generate_signature(method, url, body)
    
    return {
        'X-App-Token': SUMSUB_APP_TOKEN,
        'X-App-Access-Ts': ts,
        'X-App-Access-Sig': signature,
        'Content-Type': 'application/json'
    }

def create_applicant(external_user_id, email, level_name=None):
    """
    Cria um applicant no Sumsub
    
    Args:
        external_user_id: ID do usuário no sistema
        email: Email do usuário
        level_name: Nome do nível de verificação (opcional)
    
    Returns:
        Dict com dados do applicant criado
    """
    url = '/resources/applicants'
    method = 'POST'
    
    body = {
        'externalUserId': str(external_user_id),
        'email': email,
        'levelName': level_name or SUMSUB_LEVEL_NAME
    }
    
    try:
        headers = get_headers(method, url, body)
        response = requests.post(
            f'{SUMSUB_BASE_URL}{url}',
            json=body,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        
        logger.info(f"Applicant criado: {external_user_id}")
        return response.json()
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao criar applicant: {str(e)}")
        raise

def get_access_token(external_user_id, level_name=None, ttl_in_secs=600):
    """
    Gera token de acesso para o SDK do Sumsub
    
    Args:
        external_user_id: ID do usuário no sistema
        level_name: Nome do nível de verificação (opcional)
        ttl_in_secs: Tempo de validade do token em segundos (padrão: 10 minutos)
    
    Returns:
        Dict com token e expiração
    """
    url = f'/resources/accessTokens?userId={external_user_id}'
    
    if level_name:
        url += f'&levelName={level_name}'
    else:
        url += f'&levelName={SUMSUB_LEVEL_NAME}'
    
    url += f'&ttlInSecs={ttl_in_secs}'
    
    method = 'POST'
    
    try:
        headers = get_headers(method, url)
        response = requests.post(
            f'{SUMSUB_BASE_URL}{url}',
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        
        data = response.json()
        logger.info(f"Access token gerado para: {external_user_id}")
        
        return {
            'token': data.get('token'),
            'userId': external_user_id,
            'expiresAt': int(time.time()) + ttl_in_secs
        }
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao gerar access token: {str(e)}")
        raise

def get_applicant_status(applicant_id):
    """
    Obtém status de verificação do applicant
    
    Args:
        applicant_id: ID do applicant no Sumsub
    
    Returns:
        Dict com status da verificação
    """
    url = f'/resources/applicants/{applicant_id}/status'
    method = 'GET'
    
    try:
        headers = get_headers(method, url)
        response = requests.get(
            f'{SUMSUB_BASE_URL}{url}',
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao obter status do applicant: {str(e)}")
        raise

def get_applicant_data(applicant_id):
    """
    Obtém dados completos do applicant
    
    Args:
        applicant_id: ID do applicant no Sumsub
    
    Returns:
        Dict com dados do applicant
    """
    url = f'/resources/applicants/{applicant_id}/one'
    method = 'GET'
    
    try:
        headers = get_headers(method, url)
        response = requests.get(
            f'{SUMSUB_BASE_URL}{url}',
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao obter dados do applicant: {str(e)}")
        raise

def verify_webhook_signature(request_body, signature_header):
    """
    Verifica assinatura do webhook do Sumsub
    
    Args:
        request_body: Corpo da requisição (bytes ou string)
        signature_header: Header X-Payload-Digest (formato: "sha256=hash" ou apenas "hash")
    
    Returns:
        Boolean indicando se a assinatura é válida
    """
    if not SUMSUB_SECRET_KEY:
        raise ValueError("SUMSUB_SECRET_KEY não configurado")
    
    if isinstance(request_body, str):
        request_body = request_body.encode('utf-8')
    
    # Remover prefixo "sha256=" se presente
    received_signature = signature_header
    if received_signature.startswith('sha256='):
        received_signature = received_signature[7:]  # Remove "sha256="
    
    expected_signature = hmac.new(
        SUMSUB_SECRET_KEY.encode('utf-8'),
        request_body,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(expected_signature, received_signature)

def parse_verification_status(status_data):
    """
    Parseia status de verificação do Sumsub
    
    Args:
        status_data: Dados de status retornados pela API
    
    Returns:
        Dict com status simplificado
    """
    review_status = status_data.get('reviewStatus', 'init')
    review_result = status_data.get('reviewResult', {})
    
    # Mapeamento de status
    status_map = {
        'init': 'pending',
        'pending': 'pending',
        'queued': 'pending',
        'completed': 'approved' if review_result.get('reviewAnswer') == 'GREEN' else 'rejected',
        'onHold': 'on_hold'
    }
    
    return {
        'status': status_map.get(review_status, 'unknown'),
        'reviewStatus': review_status,
        'reviewAnswer': review_result.get('reviewAnswer'),
        'rejectLabels': review_result.get('rejectLabels', []),
        'reviewRejectType': review_result.get('reviewRejectType'),
        'moderationComment': review_result.get('moderationComment', '')
    }

def is_kyc_approved(status_data):
    """
    Verifica se o KYC foi aprovado
    
    Args:
        status_data: Dados de status retornados pela API
    
    Returns:
        Boolean indicando se o KYC foi aprovado
    """
    parsed = parse_verification_status(status_data)
    return parsed['status'] == 'approved'

def get_liveness_check_status(applicant_id):
    """
    Obtém status específico do liveness check
    
    Args:
        applicant_id: ID do applicant no Sumsub
    
    Returns:
        Dict com status do liveness check
    """
    try:
        status = get_applicant_status(applicant_id)
        
        # Verifica se há liveness check nos documentos
        liveness_status = {
            'completed': False,
            'passed': False,
            'details': None
        }
        
        if 'reviewResult' in status:
            review_result = status['reviewResult']
            
            # Verifica se há liveness check aprovado
            if review_result.get('reviewAnswer') == 'GREEN':
                liveness_status['completed'] = True
                liveness_status['passed'] = True
            elif review_result.get('reviewAnswer') in ['RED', 'YELLOW']:
                liveness_status['completed'] = True
                liveness_status['passed'] = False
                liveness_status['details'] = review_result.get('rejectLabels', [])
        
        return liveness_status
        
    except Exception as e:
        logger.error(f"Erro ao obter status do liveness check: {str(e)}")
        raise

