from flask import Blueprint, request, jsonify
import logging
from api.auth import token_required
from api.utils.db import get_db_connection
from api.utils.toolblox_client import toolblox_client, ToolbloxError

proxy_bp = Blueprint('proxy', __name__)
logger = logging.getLogger(__name__)

@proxy_bp.route('/identity', methods=['POST'])
@token_required
def mint_identity(payload):
    """Endpoint para mint de identidade via Toolblox"""
    data = request.json
    wallet = data.get('wallet')
    proof_cid = data.get('proof_cid')
    
    if not wallet or not proof_cid:
        return jsonify({'error': 'Wallet e proof_cid são obrigatórios'}), 400
    
    try:
        # Usar o novo cliente Toolblox com retry logic
        result = toolblox_client.mint_identity(wallet, proof_cid)
        
        # Salvar identidade no banco
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO identities (user_id, wallet, proof_cid, token_id, valid) VALUES (%s, %s, %s, %s, %s)',
            (payload['user_id'], wallet, proof_cid, result.get('token_id'), True)
        )
        conn.commit()
        cur.close()
        conn.close()
        
        logger.info(f"✅ Identidade mintada com sucesso para wallet {wallet}")
        return jsonify(result), 200
        
    except ToolbloxError as e:
        logger.error(f"❌ Erro do Toolblox: {e}")
        return jsonify({'error': 'Falha ao mintar identidade', 'details': str(e)}), 500
    except Exception as e:
        logger.error(f"❌ Erro inesperado: {e}")
        return jsonify({'error': 'Erro interno do servidor', 'details': str(e)}), 500

@proxy_bp.route('/signature', methods=['POST'])
@token_required
def register_signature(payload):
    """Endpoint para registro de assinatura via Toolblox"""
    data = request.json
    doc_hash = data.get('hash') or data.get('documentHash')
    signer = data.get('signer')
    
    if not doc_hash or not signer:
        return jsonify({'error': 'Hash e signer são obrigatórios'}), 400
    
    # Normalizar hash (adicionar 0x se necessário)
    if not doc_hash.startswith('0x'):
        doc_hash = '0x' + doc_hash.strip().lower()
    
    # Validar comprimento (66 caracteres: 0x + 64 hex)
    if len(doc_hash) != 66:
        return jsonify({'error': 'Hash inválido (deve ter 64 caracteres hexadecimais)'}), 400
    
    try:
        # Usar o novo cliente Toolblox com retry logic
        result = toolblox_client.register_signature(doc_hash, signer)
        
        # Salvar assinatura no banco
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO signatures (user_id, hash, tx_hash, signer) VALUES (%s, %s, %s, %s)',
            (payload['user_id'], doc_hash, result.get('tx_hash'), signer)
        )
        conn.commit()
        cur.close()
        conn.close()
        
        logger.info(f"✅ Assinatura registrada com sucesso para hash {doc_hash}")
        return jsonify(result), 200
        
    except ToolbloxError as e:
        logger.error(f"❌ Erro do Toolblox: {e}")
        return jsonify({'error': 'Falha ao registrar assinatura', 'details': str(e)}), 500
    except Exception as e:
        logger.error(f"❌ Erro inesperado: {e}")
        return jsonify({'error': 'Erro interno do servidor', 'details': str(e)}), 500

@proxy_bp.route('/verify', methods=['POST'])
@token_required
def verify_document(payload):
    """Endpoint para verificação de documento via Toolblox"""
    data = request.json
    doc_hash = data.get('hash') or data.get('documentHash')
    
    if not doc_hash:
        return jsonify({'error': 'Hash é obrigatório'}), 400
    
    # Normalizar hash (adicionar 0x se necessário)
    if not doc_hash.startswith('0x'):
        doc_hash = '0x' + doc_hash.strip().lower()
    
    # Validar comprimento (66 caracteres: 0x + 64 hex)
    if len(doc_hash) != 66:
        return jsonify({'error': 'Hash inválido (deve ter 64 caracteres hexadecimais)'}), 400
    
    try:
        # Usar o novo cliente Toolblox com retry logic
        result = toolblox_client.verify_document(doc_hash)
        
        logger.info(f"✅ Documento verificado com sucesso para hash {doc_hash}")
        return jsonify(result), 200
        
    except ToolbloxError as e:
        logger.error(f"❌ Erro do Toolblox: {e}")
        return jsonify({'error': 'Falha ao verificar documento', 'details': str(e)}), 500
    except Exception as e:
        logger.error(f"❌ Erro inesperado: {e}")
        return jsonify({'error': 'Erro interno do servidor', 'details': str(e)}), 500

