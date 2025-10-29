#!/usr/bin/env python3
"""
Script de QA para testar o fluxo completo de registro de documentos
"""

import requests
import hashlib
import json
import sys
from datetime import datetime

# Configuração
BASE_URL = "https://bts-blocktrust.onrender.com/api"
# BASE_URL = "http://localhost:5000/api"  # Para testes locais

# Cores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def log_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def log_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def log_info(message):
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")

def log_warning(message):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

def generate_fake_hash():
    """Gera um hash fake para teste"""
    timestamp = datetime.now().isoformat()
    hash_obj = hashlib.sha256(timestamp.encode())
    return '0x' + hash_obj.hexdigest()

def test_register_endpoint():
    """Testa o endpoint /api/document/register"""
    log_info("Testando endpoint /api/document/register...")
    
    # Primeiro, fazer login para obter token
    log_info("Fazendo login...")
    
    login_data = {
        "email": "admin@bts.com",
        "password": "Admin@123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        
        if response.status_code != 200:
            log_error(f"Falha no login: {response.status_code}")
            log_error(f"Response: {response.text}")
            return False
        
        token = response.json()['token']
        log_success("Login realizado com sucesso")
        
    except Exception as e:
        log_error(f"Erro ao fazer login: {str(e)}")
        return False
    
    # Gerar hash fake
    fake_hash = generate_fake_hash()
    log_info(f"Hash gerado: {fake_hash}")
    
    # Tentar registrar documento
    register_data = {
        "hash": fake_hash,
        "document_name": "test_document.pdf",
        "password": "Admin@123"
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/document/register",
            json=register_data,
            headers=headers
        )
        
        log_info(f"Status Code: {response.status_code}")
        log_info(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            log_success("✅ Registro OK - Documento registrado com sucesso!")
            return True
        else:
            log_error(f"Falha no registro: {response.status_code}")
            return False
            
    except Exception as e:
        log_error(f"Erro ao registrar documento: {str(e)}")
        return False

def test_verify_endpoint():
    """Testa o endpoint /api/document/verify"""
    log_info("Testando endpoint /api/document/verify...")
    
    # Usar um hash conhecido (do teste anterior)
    test_hash = generate_fake_hash()
    
    verify_data = {
        "hash": test_hash
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/document/verify",
            json=verify_data
        )
        
        log_info(f"Status Code: {response.status_code}")
        log_info(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            log_success("✅ Verificação OK")
            return True
        else:
            log_error(f"Falha na verificação: {response.status_code}")
            return False
            
    except Exception as e:
        log_error(f"Erro ao verificar documento: {str(e)}")
        return False

def test_history_endpoint():
    """Testa o endpoint /api/document/history"""
    log_info("Testando endpoint /api/document/history...")
    
    # Fazer login
    login_data = {
        "email": "admin@bts.com",
        "password": "Admin@123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        token = response.json()['token']
        
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        response = requests.get(
            f"{BASE_URL}/document/history",
            headers=headers
        )
        
        log_info(f"Status Code: {response.status_code}")
        log_info(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            log_success("✅ Histórico OK")
            return True
        else:
            log_error(f"Falha ao buscar histórico: {response.status_code}")
            return False
            
    except Exception as e:
        log_error(f"Erro ao buscar histórico: {str(e)}")
        return False

def main():
    """Executa todos os testes"""
    print("\n" + "="*60)
    print("🧪 QA - Teste de Registro de Documentos")
    print("="*60 + "\n")
    
    results = {
        "register": False,
        "verify": False,
        "history": False
    }
    
    # Teste 1: Registro
    print("\n📝 Teste 1: Registro de Documento")
    print("-" * 60)
    results["register"] = test_register_endpoint()
    
    # Teste 2: Verificação
    print("\n🔍 Teste 2: Verificação de Documento")
    print("-" * 60)
    results["verify"] = test_verify_endpoint()
    
    # Teste 3: Histórico
    print("\n📋 Teste 3: Histórico de Documentos")
    print("-" * 60)
    results["history"] = test_history_endpoint()
    
    # Resumo
    print("\n" + "="*60)
    print("📊 RESUMO DOS TESTES")
    print("="*60)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for test_name, passed_test in results.items():
        status = f"{Colors.GREEN}PASSOU{Colors.END}" if passed_test else f"{Colors.RED}FALHOU{Colors.END}"
        print(f"  {test_name.upper()}: {status}")
    
    print("\n" + "-"*60)
    print(f"Total: {passed}/{total} testes passaram")
    print("="*60 + "\n")
    
    # Exit code
    sys.exit(0 if passed == total else 1)

if __name__ == "__main__":
    main()

