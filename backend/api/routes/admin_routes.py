from flask import Blueprint, jsonify
from api.utils.db import get_db_connection
import os

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/migrate-kyc', methods=['GET', 'POST'])
def migrate_kyc_columns():
    """Adiciona colunas de KYC na tabela users"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Verificar se as colunas já existem
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'users'
        """)
        existing_columns = [row['column_name'] for row in cur.fetchall()]
        
        columns_to_add = []
        
        # Adicionar colunas que não existem
        if 'applicant_id' not in existing_columns:
            cur.execute("ALTER TABLE users ADD COLUMN applicant_id VARCHAR(255)")
            columns_to_add.append('applicant_id')
        
        if 'kyc_status' not in existing_columns:
            cur.execute("ALTER TABLE users ADD COLUMN kyc_status VARCHAR(50) DEFAULT 'not_started'")
            columns_to_add.append('kyc_status')
        
        if 'sumsub_data' not in existing_columns:
            cur.execute("ALTER TABLE users ADD COLUMN sumsub_data TEXT")
            columns_to_add.append('sumsub_data')
        
        if 'liveness_status' not in existing_columns:
            cur.execute("ALTER TABLE users ADD COLUMN liveness_status VARCHAR(50)")
            columns_to_add.append('liveness_status')
        
        if 'kyc_updated_at' not in existing_columns:
            cur.execute("ALTER TABLE users ADD COLUMN kyc_updated_at TIMESTAMP")
            columns_to_add.append('kyc_updated_at')
        
        conn.commit()
        
        # Verificar colunas finais
        cur.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'users'
            ORDER BY ordinal_position
        """)
        final_columns = [{'name': row['column_name'], 'type': row['data_type']} for row in cur.fetchall()]
        
        cur.close()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Migration executada com sucesso',
            'columns_added': columns_to_add,
            'total_columns': len(final_columns),
            'all_columns': final_columns
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@admin_bp.route('/debug-env', methods=['GET'])
def debug_env():
    """Retorna variáveis de ambiente para debug"""
    return jsonify({
        'toolblox': {
            'mint_url': os.getenv('TOOLBLOX_MINT_IDENTITY_URL'),
            'signature_url': os.getenv('TOOLBLOX_REGISTER_SIGNATURE_URL'),
            'verify_url': os.getenv('TOOLBLOX_VERIFY_URL'),
            'network': os.getenv('TOOLBLOX_NETWORK')
        },
        'sumsub': {
            'app_token_set': bool(os.getenv('SUMSUB_APP_TOKEN')),
            'secret_key_set': bool(os.getenv('SUMSUB_SECRET_KEY')),
            'level_name': os.getenv('SUMSUB_LEVEL_NAME')
        },
        'smtp': {
            'host': os.getenv('SMTP_HOST'),
            'port': os.getenv('SMTP_PORT'),
            'user': os.getenv('SMTP_USER'),
            'from': os.getenv('SMTP_FROM'),
            'pass_set': bool(os.getenv('SMTP_PASS'))
        }
    }), 200

