from flask import Blueprint, jsonify
from api.utils.db import get_db_connection

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

