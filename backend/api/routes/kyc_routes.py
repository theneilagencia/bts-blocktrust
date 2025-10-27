"""
Rotas para verificação KYC com Sumsub
"""
from flask import Blueprint, request, jsonify
from api.auth import token_required
from api.utils.sumsub import (
    create_applicant,
    get_access_token,
    get_applicant_status,
    get_applicant_data,
    verify_webhook_signature,
    parse_verification_status,
    is_kyc_approved,
    get_liveness_check_status
)
from api.utils.db import get_db_connection
import logging

logger = logging.getLogger(__name__)

kyc_bp = Blueprint('kyc', __name__)

@kyc_bp.route('/init', methods=['POST'])
@token_required
def init_kyc(current_user):
    """
    Inicializa processo de KYC para o usuário
    
    Returns:
        JSON com access token para o SDK do Sumsub
    """
    try:
        user_id = current_user['user_id']
        user_email = current_user['email']
        
        # Verifica se usuário já tem KYC em andamento
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT applicant_id, kyc_status, sumsub_data
            FROM users
            WHERE id = %s
        """, (user_id,))
        
        user_data = cur.fetchone()
        
        if not user_data:
            cur.close()
            conn.close()
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        applicant_id = user_data['applicant_id']
        kyc_status = user_data['kyc_status']
        
        # Se já está aprovado, retorna status
        if kyc_status == 'approved':
            cur.close()
            conn.close()
            return jsonify({
                'status': 'approved',
                'message': 'KYC já aprovado',
                'applicantId': applicant_id
            }), 200
        
        # Se não tem applicant_id, cria um novo
        if not applicant_id:
            logger.info(f"Criando applicant para usuário {user_id}")
            applicant_data = create_applicant(user_id, user_email)
            applicant_id = applicant_data.get('id')
            
            # Atualiza banco de dados
            cur.execute("""
                UPDATE users
                SET applicant_id = %s, sumsub_data = %s
                WHERE id = %s
            """, (applicant_id, str(applicant_data), user_id))
            conn.commit()
        
        # Gera access token para o SDK
        token_data = get_access_token(user_id)
        
        cur.close()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'accessToken': token_data['token'],
            'applicantId': applicant_id,
            'expiresAt': token_data['expiresAt']
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao inicializar KYC: {str(e)}")
        return jsonify({'error': 'Erro ao inicializar KYC', 'details': str(e)}), 500

@kyc_bp.route('/status', methods=['GET'])
@token_required
def get_kyc_status(current_user):
    """
    Obtém status do KYC do usuário
    
    Returns:
        JSON com status do KYC
    """
    try:
        user_id = current_user['user_id']
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT applicant_id, kyc_status, kyc_updated_at
            FROM users
            WHERE id = %s
        """, (user_id,))
        
        user_data = cur.fetchone()
        cur.close()
        conn.close()
        
        if not user_data or not user_data['applicant_id']:
            return jsonify({
                'status': 'not_started',
                'message': 'KYC não iniciado'
            }), 200
        
        applicant_id = user_data['applicant_id']
        
        # Busca status atualizado no Sumsub
        status_data = get_applicant_status(applicant_id)
        parsed_status = parse_verification_status(status_data)
        
        # Atualiza status no banco de dados
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            UPDATE users
            SET kyc_status = %s, kyc_updated_at = NOW()
            WHERE id = %s
        """, (parsed_status['status'], user_id))
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            'status': parsed_status['status'],
            'reviewStatus': parsed_status['reviewStatus'],
            'reviewAnswer': parsed_status['reviewAnswer'],
            'rejectLabels': parsed_status['rejectLabels'],
            'moderationComment': parsed_status['moderationComment'],
            'updatedAt': user_data['kyc_updated_at']
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao obter status do KYC: {str(e)}")
        return jsonify({'error': 'Erro ao obter status do KYC', 'details': str(e)}), 500

@kyc_bp.route('/liveness', methods=['GET'])
@token_required
def get_liveness_status(current_user):
    """
    Obtém status do liveness check do usuário
    
    Returns:
        JSON com status do liveness check
    """
    try:
        user_id = current_user['user_id']
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT applicant_id
            FROM users
            WHERE id = %s
        """, (user_id,))
        
        user_data = cur.fetchone()
        cur.close()
        conn.close()
        
        if not user_data or not user_data['applicant_id']:
            return jsonify({
                'completed': False,
                'passed': False,
                'message': 'KYC não iniciado'
            }), 200
        
        applicant_id = user_data['applicant_id']
        liveness_status = get_liveness_check_status(applicant_id)
        
        return jsonify(liveness_status), 200
        
    except Exception as e:
        logger.error(f"Erro ao obter status do liveness check: {str(e)}")
        return jsonify({'error': 'Erro ao obter status do liveness check', 'details': str(e)}), 500

@kyc_bp.route('/webhook', methods=['POST'])
def kyc_webhook():
    """
    Webhook para receber atualizações do Sumsub
    
    Returns:
        JSON com confirmação de recebimento
    """
    try:
        # Verifica assinatura do webhook
        signature = request.headers.get('X-Payload-Digest')
        
        if not signature:
            logger.warning("Webhook sem assinatura")
            return jsonify({'error': 'Assinatura ausente'}), 401
        
        request_body = request.get_data()
        
        if not verify_webhook_signature(request_body, signature):
            logger.warning("Assinatura inválida no webhook")
            return jsonify({'error': 'Assinatura inválida'}), 401
        
        # Processa evento
        data = request.get_json()
        
        event_type = data.get('type')
        applicant_id = data.get('applicantId')
        external_user_id = data.get('externalUserId')
        review_status = data.get('reviewStatus')
        review_result = data.get('reviewResult', {})
        
        logger.info(f"Webhook recebido: {event_type} para applicant {applicant_id}")
        
        # Atualiza status no banco de dados
        if external_user_id and review_status:
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Parseia status
            parsed_status = parse_verification_status(data)
            
            cur.execute("""
                UPDATE users
                SET kyc_status = %s,
                    kyc_updated_at = NOW(),
                    sumsub_data = %s
                WHERE id = %s
            """, (parsed_status['status'], str(data), int(external_user_id)))
            
            conn.commit()
            cur.close()
            conn.close()
            
            logger.info(f"Status KYC atualizado para usuário {external_user_id}: {parsed_status['status']}")
        
        return jsonify({'status': 'received'}), 200
        
    except Exception as e:
        logger.error(f"Erro ao processar webhook: {str(e)}")
        return jsonify({'error': 'Erro ao processar webhook', 'details': str(e)}), 500

@kyc_bp.route('/data', methods=['GET'])
@token_required
def get_kyc_data(current_user):
    """
    Obtém dados completos do KYC do usuário (apenas para admins)
    
    Returns:
        JSON com dados do KYC
    """
    try:
        # Verifica se é admin
        if current_user.get('role') != 'admin':
            return jsonify({'error': 'Acesso negado'}), 403
        
        user_id = current_user['user_id']
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT applicant_id
            FROM users
            WHERE id = %s
        """, (user_id,))
        
        user_data = cur.fetchone()
        cur.close()
        conn.close()
        
        if not user_data or not user_data['applicant_id']:
            return jsonify({'error': 'KYC não iniciado'}), 404
        
        applicant_id = user_data['applicant_id']
        applicant_data = get_applicant_data(applicant_id)
        
        return jsonify(applicant_data), 200
        
    except Exception as e:
        logger.error(f"Erro ao obter dados do KYC: {str(e)}")
        return jsonify({'error': 'Erro ao obter dados do KYC', 'details': str(e)}), 500

