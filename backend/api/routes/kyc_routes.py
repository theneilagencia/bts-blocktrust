"""
Rotas para verificação KYC com Sumsub (SEM MODO MOCK)
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
from api.utils.audit import log_kyc_event, log_nft_event
import logging

logger = logging.getLogger(__name__)

kyc_bp = Blueprint('kyc', __name__)

@kyc_bp.route('/init', methods=['POST'])
@token_required
def init_kyc(current_user):
    """
    Inicializa processo de KYC para o usuário (MODO PRODUÇÃO - SEM MOCK)
    
    Returns:
        JSON com access token para o SDK do Sumsub
    """
    try:
        # Valida credenciais do Sumsub
        is_valid, error_msg = validate_credentials()
        if not is_valid:
            logger.error(f"❌ Credenciais Sumsub inválidas: {error_msg}")
            return jsonify({
                'error': 'Configuração inválida',
                'message': 'Credenciais Sumsub não configuradas. Entre em contato com o suporte.',
                'details': error_msg
            }), 500
        
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
            logger.info(f"✅ Criando applicant para usuário {user_id}")
            
            # Criar applicant com tratamento de erro integrado
            result = create_applicant(user_id, user_email)
            
            # Verificar se houve erro
            if result.get('status') == 'error':
                error_type = result.get('type')
                error_message = result.get('message')
                error_action = result.get('action')
                
                logger.error(f"❌ {error_type}: {error_message}")
                logger.info(f"💡 Ação recomendada: {error_action}")
                
                cur.close()
                conn.close()
                
                return jsonify({
                    'error': 'Falha ao criar applicant',
                    'type': error_type,
                    'message': error_message,
                    'action': error_action
                }), 500
            
            # Sucesso
            elif result.get('status') == 'success':
                applicant_id = result.get('applicant_id')
                applicant_data = result.get('data')
                
                logger.info(f"✅ Applicant criado com sucesso: {applicant_id}")
                
                # Atualiza banco de dados
                cur.execute("""
                    UPDATE users
                    SET applicant_id = %s, sumsub_data = %s, kyc_status = 'pending'
                    WHERE id = %s
                """, (applicant_id, str(applicant_data), user_id))
                conn.commit()
            else:
                cur.close()
                conn.close()
                return jsonify({
                    'error': 'Resposta inesperada da API Sumsub',
                    'details': result
                }), 500
        
        # Gera access token para o SDK
        try:
            logger.info(f"🔑 Gerando access token para usuário {user_id}")
            token_data = get_access_token(user_id)
            logger.info(f"✅ Access token gerado com sucesso")
        except Exception as token_error:
            logger.error(f"❌ Erro ao gerar access token: {str(token_error)}")
            cur.close()
            conn.close()
            return jsonify({
                'error': 'Falha ao gerar token de acesso',
                'message': 'Não foi possível gerar token para o SDK Sumsub',
                'details': str(token_error)
            }), 500
        
        cur.close()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'accessToken': token_data['token'],
            'applicantId': applicant_id,
            'expiresAt': token_data['expiresAt'],
            'mock_mode': False
        }), 200
        
    except Exception as e:
        logger.error(f"💥 Erro ao inicializar KYC: {str(e)}")
        return jsonify({
            'error': 'Erro ao inicializar KYC',
            'details': str(e)
        }), 500

@kyc_bp.route('/status', methods=['GET'])
@token_required
def get_kyc_status(current_user):
    """
    Obtém status do KYC do usuário (MODO PRODUÇÃO - SEM MOCK)
    
    Returns:
        JSON com status da verificação
    """
    try:
        user_id = current_user['user_id']
        
        # Busca dados do usuário
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
        
        if not user_data:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        applicant_id = user_data['applicant_id']
        
        # Se não tem applicant_id, KYC não foi iniciado
        if not applicant_id:
            return jsonify({
                'status': 'not_started',
                'message': 'KYC não iniciado'
            }), 200
        
        # Busca status no Sumsub
        try:
            logger.info(f"🔍 Buscando status do applicant {applicant_id}")
            status_data = get_applicant_status(applicant_id)
            parsed_status = parse_verification_status(status_data)
            logger.info(f"✅ Status obtido: {parsed_status.get('status')}")
            
            return jsonify(parsed_status), 200
            
        except Exception as status_error:
            logger.error(f"❌ Erro ao buscar status: {str(status_error)}")
            return jsonify({
                'error': 'Falha ao buscar status',
                'message': 'Não foi possível obter status do KYC',
                'details': str(status_error)
            }), 500
        
    except Exception as e:
        logger.error(f"💥 Erro ao obter status do KYC: {str(e)}")
        return jsonify({
            'error': 'Erro ao obter status do KYC',
            'details': str(e)
        }), 500

@kyc_bp.route('/liveness', methods=['GET'])
@token_required
def get_liveness_status(current_user):
    """
    Obtém status do liveness check (MODO PRODUÇÃO - SEM MOCK)
    
    Returns:
        JSON com status do liveness check
    """
    try:
        user_id = current_user['user_id']
        
        # Busca applicant_id do usuário
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
        
        if not user_data:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        applicant_id = user_data['applicant_id']
        
        if not applicant_id:
            return jsonify({
                'completed': False,
                'message': 'KYC não iniciado'
            }), 200
        
        # Busca status do liveness check
        try:
            logger.info(f"🔍 Buscando liveness status do applicant {applicant_id}")
            liveness_status = get_liveness_check_status(applicant_id)
            logger.info(f"✅ Liveness status obtido")
            
            return jsonify(liveness_status), 200
            
        except Exception as liveness_error:
            logger.error(f"❌ Erro ao buscar liveness: {str(liveness_error)}")
            return jsonify({
                'error': 'Falha ao buscar liveness',
                'message': 'Não foi possível obter status do liveness check',
                'details': str(liveness_error)
            }), 500
        
    except Exception as e:
        logger.error(f"💥 Erro ao obter liveness status: {str(e)}")
        return jsonify({
            'error': 'Erro ao obter liveness status',
            'details': str(e)
        }), 500




@kyc_bp.route('/webhook', methods=['POST'])
def webhook():
    """
    Webhook para receber eventos do Sumsub (MODO PRODUÇÃO)
    
    Eventos suportados:
    - applicantReviewed: KYC aprovado/rejeitado
    - applicantPending: KYC em análise
    
    Returns:
        JSON com status do processamento
    """
    try:
        # Verifica assinatura do webhook
        signature = request.headers.get('X-Payload-Digest')
        
        if not signature:
            logger.warning("❌ Webhook sem assinatura")
            return jsonify({'error': 'Assinatura ausente'}), 401
        
        request_body = request.get_data()
        
        # Verificar assinatura
        signature_valid = verify_webhook_signature(request_body, signature)
        
        if not signature_valid:
            logger.error(f"❌ Assinatura HMAC inválida no webhook")
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
        
        logger.info(f"✅ Webhook recebido: {event_type} para applicant {applicant_id}")
        
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
            
            logger.info(f"✅ Status KYC atualizado para usuário {external_user_id}: {parsed_status['status']}")
            
            # Registrar evento de auditoria
            log_kyc_event(
                user_id=int(external_user_id),
                event_type=parsed_status['status'],
                applicant_id=applicant_id,
                review_status=review_status,
                details={'review_result': review_result}
            )
            
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
                        
                        # Registrar evento de auditoria do NFT
                        log_nft_event(
                            user_id=int(external_user_id),
                            event_type='minted',
                            nft_id=mint_result['nft_id'],
                            tx_hash=mint_result['tx_hash'],
                            details={'kyc_applicant_id': applicant_id}
                        )
                    else:
                        logger.error(f"❌ Erro ao mintar NFT: {mint_result.get('error')}")
                        
                except Exception as nft_error:
                    logger.error(f"❌ Erro no processo de NFT: {str(nft_error)}")
                    # Não falhar o webhook por causa do NFT
        
        return jsonify({'status': 'received'}), 200
        
    except Exception as e:
        logger.error(f"💥 Erro ao processar webhook: {str(e)}")
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
        
        try:
            logger.info(f"🔍 Buscando dados do applicant {applicant_id}")
            applicant_data = get_applicant_data(applicant_id)
            logger.info(f"✅ Dados obtidos com sucesso")
            
            return jsonify(applicant_data), 200
            
        except Exception as data_error:
            logger.error(f"❌ Erro ao buscar dados: {str(data_error)}")
            return jsonify({
                'error': 'Falha ao buscar dados',
                'message': 'Não foi possível obter dados do applicant',
                'details': str(data_error)
            }), 500
        
    except Exception as e:
        logger.error(f"💥 Erro ao obter dados do KYC: {str(e)}")
        return jsonify({'error': 'Erro ao obter dados do KYC', 'details': str(e)}), 500

