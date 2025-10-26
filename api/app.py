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

@app.route('/api/init-db', methods=['POST'])
def initialize_database():
    try:
        init_db()
        return jsonify({'status': 'success', 'message': 'Database initialized successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Inicialização do banco de dados comentada temporariamente
# @app.before_request
# def before_first_request():
#     init_db()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

