from flask import Blueprint, request, jsonify
import requests
import os
from auth import token_required
from utils.db import get_db_connection

proxy_bp = Blueprint('proxy', __name__)

TOOLBLOX_MINT_URL = os.getenv('TOOLBLOX_MINT_IDENTITY_URL')
TOOLBLOX_SIGNATURE_URL = os.getenv('TOOLBLOX_REGISTER_SIGNATURE_URL')
TOOLBLOX_VERIFY_URL = os.getenv('TOOLBLOX_VERIFY_URL')

@proxy_bp.route('/identity', methods=['POST'])
@token_required
def mint_identity(payload):
    data = request.json
    wallet = data.get('wallet')
    proof_cid = data.get('proof_cid')
    
    if not wallet or not proof_cid:
        return jsonify({'error': 'Wallet e proof_cid são obrigatórios'}), 400
    
    try:
        response = requests.post(TOOLBLOX_MINT_URL, json={
            'wallet': wallet,
            'proof_cid': proof_cid
        }, timeout=30)
        
        result = response.json()
        
        if response.status_code == 200:
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
        
        return jsonify(result), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@proxy_bp.route('/signature', methods=['POST'])
@token_required
def register_signature(payload):
    data = request.json
    doc_hash = data.get('hash')
    signer = data.get('signer')
    
    if not doc_hash or not signer:
        return jsonify({'error': 'Hash e signer são obrigatórios'}), 400
    
    try:
        response = requests.post(TOOLBLOX_SIGNATURE_URL, json={
            'hash': doc_hash,
            'signer': signer
        }, timeout=30)
        
        result = response.json()
        
        if response.status_code == 200:
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
        
        return jsonify(result), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@proxy_bp.route('/verify', methods=['POST'])
@token_required
def verify_document(payload):
    data = request.json
    doc_hash = data.get('hash')
    
    if not doc_hash:
        return jsonify({'error': 'Hash é obrigatório'}), 400
    
    try:
        response = requests.post(TOOLBLOX_VERIFY_URL, json={
            'hash': doc_hash
        }, timeout=30)
        
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

