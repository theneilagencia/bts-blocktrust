import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from routes.auth_routes import auth_bp
from routes.proxy_routes import proxy_bp
from routes.panic_routes import panic_bp
from utils.db import init_db

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = os.getenv('JWT_SECRET', 'dev-secret-key')

# Registrar blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(proxy_bp, url_prefix='/api/proxy')
app.register_blueprint(panic_bp, url_prefix='/api')

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'service': 'BTS Blocktrust API'})

@app.route('/api/init-db', methods=['POST', 'GET'])
def initialize_database():
    import os
    db_url = os.getenv('DATABASE_URL', 'NOT_SET')
    try:
        init_db()
        return jsonify({
            'status': 'success', 
            'message': 'Database initialized successfully',
            'db_host': db_url.split('@')[1].split('/')[0] if '@' in db_url else 'unknown'
        })
    except Exception as e:
        return jsonify({
            'status': 'error', 
            'message': str(e),
            'db_url_set': db_url != 'NOT_SET',
            'db_host': db_url.split('@')[1].split('/')[0] if '@' in db_url and len(db_url.split('@')) > 1 else 'unknown'
        }), 500

# Inicialização do banco de dados comentada temporariamente
# @app.before_request
# def before_first_request():
#     init_db()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

