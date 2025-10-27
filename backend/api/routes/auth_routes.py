from flask import Blueprint, request, jsonify
import bcrypt
from auth import generate_token, token_required
from utils.db import get_db_connection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email e senha são obrigatórios'}), 400
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Verificar se usuário já existe
    cur.execute('SELECT id FROM users WHERE email = %s', (email,))
    if cur.fetchone():
        cur.close()
        conn.close()
        return jsonify({'error': 'Email já cadastrado'}), 409
    
    # Hash da senha
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Inserir usuário
    cur.execute(
        'INSERT INTO users (email, password_hash, role) VALUES (%s, %s, %s) RETURNING id',
        (email, password_hash, 'user')
    )
    user_id = cur.fetchone()[0]
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
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('SELECT id, password_hash, role FROM users WHERE email = %s', (email,))
    user = cur.fetchone()
    
    cur.close()
    conn.close()
    
    if not user:
        return jsonify({'error': 'Credenciais inválidas'}), 401
    
    user_id, password_hash, role = user
    
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

