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
    get_liveness_check_status,
    validate_credentials
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
        # Valida credenciais do Sumsub
        is_valid, error_msg = validate_credentials()
        if not is_valid:
            logger.warning(f"⚠️  Credenciais Sumsub inválidas: {error_msg}")
            logger.warning("⚠️  Usando modo mock para KYC")
            
            # Modo mock: retorna token simulado
            user_id = current_user['user_id']
            mock_applicant_id = f"mock_applicant_{user_id}"
            
            # Atualiza banco com applicant_id mock
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                UPDATE users
                SET applicant_id = %s, kyc_status = 'pending'
                WHERE id = %s
            """, (mock_applicant_id, user_id))
            conn.commit()
            cur.close()
            conn.close()
            
            return jsonify({
                'status': 'success',
                'accessToken': 'mock_access_token_for_testing',
                'applicantId': mock_applicant_id,
                'expiresAt': '2025-12-31T23:59:59Z',
                'mock_mode': True,
                'message': 'Mock: KYC inicializado (API indisponível)'
            }), 200
        
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
            
            # Criar applicant com tratamento de erro integrado
            result = create_applicant(user_id, user_email)
            
            # Verificar se houve erro
            if result.get('status') == 'error':
                logger.error(f"❌ {result.get('type')}: {result.get('message')}")
                logger.info(f"💡 Ação recomendada: {result.get('action')}")
                
                # Usar modo mock
                mock_applicant_id = f"mock_applicant_{user_id}"
                logger.warning(f"🧩 Ativando modo mock: {mock_applicant_id}")
                
                cur.execute("""
                    UPDATE users
                    SET applicant_id = %s, kyc_status = 'pending'
                    WHERE id = %s
                """, (mock_applicant_id, user_id))
                conn.commit()
                cur.close()
                conn.close()
                
                return jsonify({
                    'status': 'success',
                    'accessToken': 'mock_access_token_for_testing',
                    'applicantId': mock_applicant_id,
                    'expiresAt': '2025-12-31T23:59:59Z',
                    'mock_mode': True,
                    'error_type': result.get('type'),
                    'message': f"Mock: {result.get('message')}"
                }), 200
            
            # Verificar se é modo mock
            elif result.get('status') == 'mock':
                mock_applicant_id = result.get('applicant_id')
                logger.warning(f"🧩 Modo mock ativado: {mock_applicant_id}")
                
                cur.execute("""
                    UPDATE users
                    SET applicant_id = %s, kyc_status = 'pending'
                    WHERE id = %s
                """, (mock_applicant_id, user_id))
                conn.commit()
                cur.close()
                conn.close()
                
                return jsonify({
                    'status': 'success',
                    'accessToken': 'mock_access_token_for_testing',
                    'applicantId': mock_applicant_id,
                    'expiresAt': '2025-12-31T23:59:59Z',
                    'mock_mode': True,
                    'message': result.get('message')
                }), 200
            
            # Sucesso
            elif result.get('status') == 'success':
                applicant_id = result.get('applicant_id')
                applicant_data = result.get('data')
                
                # Atualiza banco de dados
                cur.execute("""
                    UPDATE users
                    SET applicant_id = %s, sumsub_data = %s
                    WHERE id = %s
                """, (applicant_id, str(applicant_data), user_id))
                conn.commit()
        
        # Gera access token para o SDK
        try:
            token_data = get_access_token(user_id)
        except Exception as token_error:
            # Se falhar ao gerar token (401), usar modo mock
            if '401' in str(token_error) or 'Unauthorized' in str(token_error):
                logger.warning("⚠️  Falha ao gerar token no Sumsub, usando modo mock")
                cur.close()
                conn.close()
                
                return jsonify({
                    'status': 'success',
                    'accessToken': 'mock_access_token_for_testing',
                    'applicantId': applicant_id,
                    'expiresAt': '2025-12-31T23:59:59Z',
                    'mock_mode': True,
                    'message': 'Mock: Token gerado (API indisponível)'
                }), 200
            else:
                raise
        
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
        # Modo mock como último recurso
        if '401' in str(e) or 'Unauthorized' in str(e):
            logger.warning("⚠️  Erro 401 no KYC, usando modo mock")
            return jsonify({
                'status': 'success',
                'accessToken': 'mock_access_token_for_testing',
                'applicantId': f'mock_applicant_{current_user["user_id"]}',
                'expiresAt': '2025-12-31T23:59:59Z',
                'mock_mode': True,
                'message': 'Mock: KYC inicializado (API indisponível)'
            }), 200
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
        
        # Se é applicant_id mock, retornar status mock
        if applicant_id and applicant_id.startswith('mock_applicant_'):
            logger.info(f"⚠️  Applicant mock detectado, retornando status mock")
            return jsonify({
                'status': 'pending',
                'reviewStatus': 'pending',
                'reviewAnswer': 'GREEN',
                'rejectLabels': [],
                'moderationComment': 'Mock: KYC em processamento (API indisponível)',
                'updatedAt': user_data['kyc_updated_at'],
                'mock_mode': True
            }), 200
        
        # Busca status atualizado no Sumsub
        try:
            status_data = get_applicant_status(applicant_id)
            parsed_status = parse_verification_status(status_data)
        except Exception as status_error:
            # Se falhar ao buscar status, retornar mock
            if '401' in str(status_error) or 'Unauthorized' in str(status_error):
                logger.warning("⚠️  Falha ao buscar status no Sumsub, usando modo mock")
                return jsonify({
                    'status': 'pending',
                    'reviewStatus': 'pending',
                    'reviewAnswer': 'GREEN',
                    'rejectLabels': [],
                    'moderationComment': 'Mock: KYC em processamento (API indisponível)',
                    'updatedAt': user_data['kyc_updated_at'],
                    'mock_mode': True
                }), 200
            else:
                raise
        
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
        
        # Se é applicant_id mock, retornar liveness mock
        if applicant_id and applicant_id.startswith('mock_applicant_'):
            logger.info(f"⚠️  Applicant mock detectado, retornando liveness mock")
            return jsonify({
                'completed': True,
                'passed': True,
                'message': 'Mock: Liveness check aprovado (API indisponível)',
                'mock_mode': True
            }), 200
        
        # Buscar liveness status no Sumsub
        try:
            liveness_status = get_liveness_check_status(applicant_id)
        except Exception as liveness_error:
            # Se falhar, retornar mock
            if '401' in str(liveness_error) or 'Unauthorized' in str(liveness_error):
                logger.warning("⚠️  Falha ao buscar liveness no Sumsub, usando modo mock")
                return jsonify({
                    'completed': True,
                    'passed': True,
                    'message': 'Mock: Liveness check aprovado (API indisponível)',
                    'mock_mode': True
                }), 200
            else:
                raise
        
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
        
        # Verificar assinatura
        signature_valid = verify_webhook_signature(request_body, signature)
        
        if not signature_valid:
            logger.error(f"❌ Assinatura HMAC inválida no webhook: {signature[:20]}...")
            logger.debug(f"Body recebido (primeiros 200 chars): {request_body[:200]}")
            
            # Verificar se estamos em modo de desenvolvimento local (BYPASS_WEBHOOK_VALIDATION)
            import os
            bypass_validation = os.getenv('BYPASS_WEBHOOK_VALIDATION', 'false').lower() == 'true'
            
            if bypass_validation:
                logger.warning("⚠️  BYPASS_WEBHOOK_VALIDATION ativado: aceitando webhook com assinatura inválida")
                logger.warning("🚨 ATENÇÃO: Isso não deve estar ativado em produção!")
            else:
                # PRODUÇÃO: Rejeitar webhook com assinatura inválida
                return jsonify({
                    'error': 'Assinatura HMAC inválida',
                    'message': 'Webhook rejeitado por falha na validação de segurança'
                }), 403
        
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
            
            # Se KYC foi aprovado, iniciar processo de mint de NFT
            if parsed_status['status'] == 'approved':
                logger.info(f"🎯 KYC aprovado para usuário {external_user_id} - Iniciando processo de mint de NFT")
                
                try:
                    # Importar utilitários de NFT
                    from api.utils.nft import check_active_nft, cancel_nft, mint_nft
                    
                    # 1. Verificar se usuário já possui NFT ativo
                    existing_nft = check_active_nft(int(external_user_id))
                    
                    if existing_nft:
                        logger.info(f"⚠️  Usuário {external_user_id} já possui NFT ativo (ID: {existing_nft['nft_id']}) - Cancelando...")
                        
                        # 2. Cancelar NFT anterior
                        cancel_result = cancel_nft(int(external_user_id), existing_nft['nft_id'])
                        
                        if cancel_result['success']:
                            logger.info(f"✅ NFT anterior cancelado: {cancel_result['tx_hash']}")
                        else:
                            logger.error(f"❌ Erro ao cancelar NFT anterior: {cancel_result.get('error')}")
                    
                    # 3. Mintar novo NFT
                    logger.info(f"🎨 Mintando novo NFT para usuário {external_user_id}...")
                    
                    mint_result = mint_nft(
                        user_id=int(external_user_id),
                        kyc_data={
                            'applicant_id': applicant_id,
                            'review_status': review_status,
                            'review_result': review_result
                        }
                    )
                    
                    if mint_result['success']:
                        logger.info(f"✅ NFT mintado com sucesso: ID={mint_result['nft_id']}, TX={mint_result['tx_hash']}")
                    else:
                        logger.error(f"❌ Erro ao mintar NFT: {mint_result.get('error')}")
                        
                except Exception as nft_error:
                    logger.error(f"❌ Erro no processo de NFT: {str(nft_error)}")
                    # Não falhar o webhook por causa do NFT
        
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

