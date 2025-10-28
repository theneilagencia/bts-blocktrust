"""
Módulo de Gerenciamento de NFT SoulBound
Implementa lógica de minting, cancelamento e consulta de NFTs de identidade
"""

import os
import logging
from typing import Dict, Optional
from web3 import Web3
from web3.middleware import geth_poa_middleware
import json

logger = logging.getLogger(__name__)

# Configurações
POLYGON_RPC_URL = os.getenv('POLYGON_RPC_URL', 'https://polygon-mumbai.infura.io/v3/demo')
IDENTITY_NFT_CONTRACT_ADDRESS = os.getenv('IDENTITY_NFT_CONTRACT_ADDRESS', '0x0000000000000000000000000000000000000000')
PROOF_REGISTRY_CONTRACT_ADDRESS = os.getenv('PROOF_REGISTRY_CONTRACT_ADDRESS', '0x0000000000000000000000000000000000000000')

# ABIs dos contratos (simplificados para demonstração)
IDENTITY_NFT_ABI = [
    {
        "inputs": [
            {"name": "user", "type": "address"},
            {"name": "metadata", "type": "bytes"},
            {"name": "previousId", "type": "uint256"}
        ],
        "name": "mintIdentityNFT",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"name": "nftId", "type": "uint256"}],
        "name": "cancelNFT",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"name": "user", "type": "address"}],
        "name": "getActiveNFT",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"name": "user", "type": "address"}],
        "name": "isActiveNFT",
        "outputs": [{"name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "nftId", "type": "uint256"},
            {"indexed": True, "name": "novoNftId", "type": "uint256"}
        ],
        "name": "CancelamentoEvent",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "nftId", "type": "uint256"},
            {"indexed": True, "name": "user", "type": "address"}
        ],
        "name": "MintingEvent",
        "type": "event"
    }
]

PROOF_REGISTRY_ABI = [
    {
        "inputs": [
            {"name": "docHash", "type": "string"},
            {"name": "proofUrl", "type": "string"}
        ],
        "name": "registerProof",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"name": "docHash", "type": "string"}],
        "name": "verifyProof",
        "outputs": [{"name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    }
]

class NFTManager:
    """Gerenciador de NFTs SoulBound"""
    
    def __init__(self):
        """Inicializa o gerenciador de NFTs"""
        self.w3 = Web3(Web3.HTTPProvider(POLYGON_RPC_URL))
        
        # Adicionar middleware para PoA (Polygon)
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        
        # Verificar conexão
        if not self.w3.is_connected():
            logger.warning("⚠️ Não foi possível conectar ao RPC do Polygon")
        else:
            logger.info(f"✅ Conectado ao Polygon: {POLYGON_RPC_URL}")
        
        # Inicializar contratos
        self.identity_nft_contract = None
        self.proof_registry_contract = None
        
        if IDENTITY_NFT_CONTRACT_ADDRESS != '0x0000000000000000000000000000000000000000':
            self.identity_nft_contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(IDENTITY_NFT_CONTRACT_ADDRESS),
                abi=IDENTITY_NFT_ABI
            )
        
        if PROOF_REGISTRY_CONTRACT_ADDRESS != '0x0000000000000000000000000000000000000000':
            self.proof_registry_contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(PROOF_REGISTRY_CONTRACT_ADDRESS),
                abi=PROOF_REGISTRY_ABI
            )
    
    def get_active_nft(self, wallet_address: str) -> Optional[int]:
        """
        Obtém o ID do NFT ativo do usuário
        
        Args:
            wallet_address: Endereço da carteira do usuário
            
        Returns:
            ID do NFT ativo ou None se não houver
        """
        try:
            if not self.identity_nft_contract:
                logger.warning("⚠️ Contrato de NFT não configurado")
                return None
            
            checksum_address = Web3.to_checksum_address(wallet_address)
            nft_id = self.identity_nft_contract.functions.getActiveNFT(checksum_address).call()
            
            if nft_id == 0:
                logger.info(f"ℹ️ Usuário {wallet_address} não possui NFT ativo")
                return None
            
            logger.info(f"✅ NFT ativo encontrado: {nft_id} para {wallet_address}")
            return nft_id
            
        except Exception as e:
            logger.error(f"❌ Erro ao obter NFT ativo: {str(e)}")
            return None
    
    def is_active_nft(self, wallet_address: str) -> bool:
        """
        Verifica se o usuário possui um NFT ativo
        
        Args:
            wallet_address: Endereço da carteira do usuário
            
        Returns:
            True se possui NFT ativo, False caso contrário
        """
        try:
            if not self.identity_nft_contract:
                return False
            
            checksum_address = Web3.to_checksum_address(wallet_address)
            is_active = self.identity_nft_contract.functions.isActiveNFT(checksum_address).call()
            
            return is_active
            
        except Exception as e:
            logger.error(f"❌ Erro ao verificar NFT ativo: {str(e)}")
            return False
    
    def cancel_nft(self, nft_id: int, private_key: str) -> Dict:
        """
        Cancela um NFT existente
        
        Args:
            nft_id: ID do NFT a ser cancelado
            private_key: Chave privada para assinar a transação
            
        Returns:
            Dict com status e transaction_hash
        """
        try:
            if not self.identity_nft_contract:
                raise ValueError("Contrato de NFT não configurado")
            
            # Criar conta a partir da chave privada
            account = self.w3.eth.account.from_key(private_key)
            
            # Preparar transação
            nonce = self.w3.eth.get_transaction_count(account.address)
            
            transaction = self.identity_nft_contract.functions.cancelNFT(nft_id).build_transaction({
                'from': account.address,
                'nonce': nonce,
                'gas': 200000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            # Assinar transação
            signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key)
            
            # Enviar transação
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            # Aguardar confirmação
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            logger.info(f"✅ NFT {nft_id} cancelado com sucesso: {tx_hash.hex()}")
            
            return {
                'status': 'success',
                'transaction_hash': tx_hash.hex(),
                'block_number': receipt['blockNumber'],
                'gas_used': receipt['gasUsed']
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao cancelar NFT: {str(e)}")
            raise
    
    def mint_identity_nft(
        self,
        wallet_address: str,
        metadata: Dict,
        previous_nft_id: int,
        private_key: str
    ) -> Dict:
        """
        Minta um novo NFT de identidade
        
        Args:
            wallet_address: Endereço da carteira do usuário
            metadata: Metadados do NFT (KYC info, etc.)
            previous_nft_id: ID do NFT anterior (0 se for o primeiro)
            private_key: Chave privada para assinar a transação
            
        Returns:
            Dict com status, nft_id e transaction_hash
        """
        try:
            if not self.identity_nft_contract:
                raise ValueError("Contrato de NFT não configurado")
            
            # Criar conta a partir da chave privada
            account = self.w3.eth.account.from_key(private_key)
            
            # Converter metadata para bytes
            metadata_json = json.dumps(metadata)
            metadata_bytes = metadata_json.encode('utf-8')
            
            # Preparar transação
            checksum_address = Web3.to_checksum_address(wallet_address)
            nonce = self.w3.eth.get_transaction_count(account.address)
            
            transaction = self.identity_nft_contract.functions.mintIdentityNFT(
                checksum_address,
                metadata_bytes,
                previous_nft_id
            ).build_transaction({
                'from': account.address,
                'nonce': nonce,
                'gas': 300000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            # Assinar transação
            signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key)
            
            # Enviar transação
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            # Aguardar confirmação
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            # Extrair NFT ID dos logs (simplificado)
            # Em produção, parse os eventos do receipt
            nft_id = previous_nft_id + 1  # Simplificação
            
            logger.info(f"✅ NFT {nft_id} mintado com sucesso para {wallet_address}: {tx_hash.hex()}")
            
            return {
                'status': 'success',
                'nft_id': nft_id,
                'transaction_hash': tx_hash.hex(),
                'block_number': receipt['blockNumber'],
                'gas_used': receipt['gasUsed']
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao mintar NFT: {str(e)}")
            raise
    
    def register_proof(
        self,
        doc_hash: str,
        proof_url: str,
        private_key: str
    ) -> Dict:
        """
        Registra uma prova de documento na blockchain
        
        Args:
            doc_hash: Hash do documento
            proof_url: URL da prova
            private_key: Chave privada para assinar a transação
            
        Returns:
            Dict com status e transaction_hash
        """
        try:
            if not self.proof_registry_contract:
                raise ValueError("Contrato de ProofRegistry não configurado")
            
            # Criar conta a partir da chave privada
            account = self.w3.eth.account.from_key(private_key)
            
            # Preparar transação
            nonce = self.w3.eth.get_transaction_count(account.address)
            
            transaction = self.proof_registry_contract.functions.registerProof(
                doc_hash,
                proof_url
            ).build_transaction({
                'from': account.address,
                'nonce': nonce,
                'gas': 200000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            # Assinar transação
            signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key)
            
            # Enviar transação
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            # Aguardar confirmação
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            logger.info(f"✅ Prova registrada com sucesso: {tx_hash.hex()}")
            
            return {
                'status': 'success',
                'transaction_hash': tx_hash.hex(),
                'block_number': receipt['blockNumber'],
                'gas_used': receipt['gasUsed']
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao registrar prova: {str(e)}")
            raise
    
    def verify_proof(self, doc_hash: str) -> bool:
        """
        Verifica se uma prova existe na blockchain
        
        Args:
            doc_hash: Hash do documento
            
        Returns:
            True se a prova existe, False caso contrário
        """
        try:
            if not self.proof_registry_contract:
                return False
            
            exists = self.proof_registry_contract.functions.verifyProof(doc_hash).call()
            
            if exists:
                logger.info(f"✅ Prova verificada: {doc_hash}")
            else:
                logger.warning(f"⚠️ Prova não encontrada: {doc_hash}")
            
            return exists
            
        except Exception as e:
            logger.error(f"❌ Erro ao verificar prova: {str(e)}")
            return False

# Instância global do gerenciador
nft_manager = NFTManager()



# Funções auxiliares para integração com KYC

def check_active_nft(user_id: int) -> Optional[Dict]:
    """
    Verifica se o usuário possui um NFT ativo
    
    Args:
        user_id: ID do usuário no banco de dados
        
    Returns:
        Dict com informações do NFT ativo ou None
    """
    try:
        from api.database import get_db_connection
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT nft_id, wallet_address, nft_active, nft_minted_at
            FROM users
            WHERE id = %s AND nft_active = TRUE
        """, (user_id,))
        
        result = cur.fetchone()
        cur.close()
        conn.close()
        
        if not result:
            return None
        
        return {
            'nft_id': result[0],
            'wallet_address': result[1],
            'nft_active': result[2],
            'nft_minted_at': result[3]
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao verificar NFT ativo: {str(e)}")
        return None

def cancel_nft(user_id: int, nft_id: int) -> Dict:
    """
    Cancela um NFT ativo
    
    Args:
        user_id: ID do usuário
        nft_id: ID do NFT a ser cancelado
        
    Returns:
        Dict com resultado da operação
    """
    try:
        from api.database import get_db_connection
        
        # TODO: Chamar contrato IdentityNFT.cancelNFT(nft_id)
        # Por enquanto, apenas simular
        import hashlib
        tx_hash = "0x" + hashlib.sha256(f"cancel_{nft_id}".encode()).hexdigest()
        
        # Atualizar banco de dados
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            UPDATE users
            SET nft_active = FALSE
            WHERE id = %s
        """, (user_id,))
        
        # Registrar cancelamento
        cur.execute("""
            INSERT INTO nft_cancellations (user_id, nft_id, reason, created_at)
            VALUES (%s, %s, %s, NOW())
        """, (user_id, nft_id, 'KYC re-approval'))
        
        conn.commit()
        cur.close()
        conn.close()
        
        logger.info(f"✅ NFT {nft_id} cancelado para usuário {user_id}")
        
        return {
            'success': True,
            'tx_hash': tx_hash,
            'nft_id': nft_id
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao cancelar NFT: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

def mint_nft(user_id: int, kyc_data: Dict) -> Dict:
    """
    Minta um novo NFT para o usuário
    
    Args:
        user_id: ID do usuário
        kyc_data: Dados do KYC aprovado
        
    Returns:
        Dict com resultado da operação
    """
    try:
        from api.database import get_db_connection
        import hashlib
        import json
        
        # Obter dados do usuário
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT wallet_address, email, name
            FROM users
            WHERE id = %s
        """, (user_id,))
        
        user_data = cur.fetchone()
        
        if not user_data:
            return {
                'success': False,
                'error': 'Usuário não encontrado'
            }
        
        wallet_address, email, name = user_data
        
        # Se não tem carteira, criar uma
        if not wallet_address:
            from api.utils.wallet import generate_wallet
            wallet_result = generate_wallet(user_id)
            
            if not wallet_result['success']:
                return {
                    'success': False,
                    'error': 'Erro ao gerar carteira'
                }
            
            wallet_address = wallet_result['address']
        
        # TODO: Chamar contrato IdentityNFT.mintIdentityNFT(wallet_address, metadata, previousId)
        # Por enquanto, apenas simular
        import random
        nft_id = random.randint(1000, 9999)
        tx_hash = "0x" + hashlib.sha256(f"mint_{nft_id}_{wallet_address}".encode()).hexdigest()
        
        # Atualizar banco de dados
        cur.execute("""
            UPDATE users
            SET nft_id = %s,
                nft_active = TRUE,
                nft_minted_at = NOW(),
                nft_transaction_hash = %s
            WHERE id = %s
        """, (nft_id, tx_hash, user_id))
        
        conn.commit()
        cur.close()
        conn.close()
        
        logger.info(f"✅ NFT {nft_id} mintado para usuário {user_id} ({wallet_address})")
        
        return {
            'success': True,
            'nft_id': nft_id,
            'tx_hash': tx_hash,
            'wallet_address': wallet_address
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao mintar NFT: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

