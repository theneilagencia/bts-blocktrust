import os
import requests
import time
import hmac
import hashlib

SUMSUB_APP_TOKEN = os.getenv('SUMSUB_APP_TOKEN')
SUMSUB_SECRET_KEY = os.getenv('SUMSUB_SECRET_KEY')
SUMSUB_BASE_URL = 'https://api.sumsub.com'

def generate_signature(method, url, body=''):
    """Gera assinatura para requisições Sumsub"""
    ts = str(int(time.time()))
    signature_string = f'{ts}{method}{url}{body}'
    signature = hmac.new(
        SUMSUB_SECRET_KEY.encode('utf-8'),
        signature_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return ts, signature

def create_applicant(external_user_id, email):
    """Cria um applicant no Sumsub"""
    url = '/resources/applicants'
    method = 'POST'
    body = {
        'externalUserId': external_user_id,
        'email': email
    }
    
    ts, signature = generate_signature(method, url, str(body))
    
    headers = {
        'X-App-Token': SUMSUB_APP_TOKEN,
        'X-App-Access-Ts': ts,
        'X-App-Access-Sig': signature,
        'Content-Type': 'application/json'
    }
    
    response = requests.post(f'{SUMSUB_BASE_URL}{url}', json=body, headers=headers)
    return response.json()

def get_applicant_status(applicant_id):
    """Obtém status de verificação do applicant"""
    url = f'/resources/applicants/{applicant_id}/status'
    method = 'GET'
    
    ts, signature = generate_signature(method, url)
    
    headers = {
        'X-App-Token': SUMSUB_APP_TOKEN,
        'X-App-Access-Ts': ts,
        'X-App-Access-Sig': signature
    }
    
    response = requests.get(f'{SUMSUB_BASE_URL}{url}', headers=headers)
    return response.json()

