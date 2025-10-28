from flask import Blueprint, request, jsonify
import bcrypt
import re
from api.auth import generate_token, token_required
from api.utils.db import get_db_connection

auth_bp = Blueprint('auth', __name__)

def sanitize_email(email):
    """
    Sanitiza email removendo caracteres perigosos (XSS)
    
    Args:
        email: Email a ser sanitizado
    
    Returns:
        Email sanitizado ou None se inválido
    """
    if not email:
        return None
    
    # Remove espaços em branco
    email = email.strip()
    
    # Verifica se contém tags HTML ou scripts
    if re.search(r'<[^>]+>', email):
        return None
    
    # Valida formato básico de email
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return None
    
    return email.lower()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    coercion_password = data.get('coercion_password')  # Senha de coação
    
    if not email or not password:
        return jsonify({'error': 'Email e senha são obrigatórios'}), 400
    
    if not coercion_password:
        return jsonify({'error': 'Senha de coação é obrigatória'}), 400
    
    # Validar que as senhas são diferentes
    if password == coercion_password:
        return jsonify({'error': 'Senha de coação deve ser diferente da senha normal'}), 400
    
    # Sanitizar email (proteção XSS)
    email = sanitize_email(email)
    if not email:
        return jsonify({'error': 'Email inválido ou contém caracteres não permitidos'}), 400
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Verificar se usuário já existe
    cur.execute('SELECT id FROM users WHERE email = %s', (email,))
    if cur.fetchone():
        cur.close()
        conn.close()
        return jsonify({'error': 'Email já cadastrado'}), 409
    
    # Hash das senhas (normal e de coação)
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    coercion_hash = bcrypt.hashpw(coercion_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Inserir usuário com ambas as senhas
    cur.execute(
        '''INSERT INTO users (email, password_hash, failsafe_password_hash, failsafe_configured, role) 
           VALUES (%s, %s, %s, TRUE, %s) RETURNING id''',
        (email, password_hash, coercion_hash, 'user')
    )
    result = cur.fetchone()
    user_id = result['id']
    conn.commit()
    cur.close()
    conn.close()
    
    token = generate_token(user_id, email, 'user')
    
    return jsonify({
        'message': 'Usuário cadastrado com sucesso',
        'token': token,
        'user': {'id': user_id, 'email': email, 'role': 'user'}
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email e senha são obrigatórios'}), 400
    
    # Sanitizar email (proteção XSS)
    email = sanitize_email(email)
    if not email:
        return jsonify({'error': 'Email inválido ou contém caracteres não permitidos'}), 400
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('SELECT id, password_hash, role FROM users WHERE email = %s', (email,))
    user = cur.fetchone()
    
    cur.close()
    conn.close()
    
    if not user:
        return jsonify({'error': 'Credenciais inválidas'}), 401
    
    user_id = user['id']
    password_hash = user['password_hash']
    role = user['role']
    
    if not bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
        return jsonify({'error': 'Credenciais inválidas'}), 401
    
    token = generate_token(user_id, email, role)
    
    return jsonify({
        'message': 'Login realizado com sucesso',
        'token': token,
        'user': {'id': user_id, 'email': email, 'role': role}
    }), 200

@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user(payload):
    return jsonify({
        'user': {
            'id': payload['user_id'],
            'email': payload['email'],
            'role': payload['role']
        }
    }), 200

