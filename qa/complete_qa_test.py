#!/usr/bin/env python3
"""
Script completo de QA para BTS Blocktrust
Testa backend, frontend, KYC, blockchain e segurança
"""

import requests
import json
import time
import hmac
import hashlib
import os
from datetime import datetime
from typing import Dict, List, Any

# Configurações
BASE_URL = "https://bts-blocktrust.onrender.com"
API_URL = f"{BASE_URL}/api"
SUMSUB_SECRET = os.getenv('SUMSUB_SECRET_KEY', 'HPuMPbFC5s1dgqbgDRIVJu5JP82eLgFc')

# Resultados
results = {
    "timestamp": datetime.now().isoformat(),
    "tests": [],
    "summary": {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "warnings": 0
    },
    "latency": {}
}

def log_test(module: str, test_name: str, status: str, latency: float, details: str = ""):
    """Registra resultado de um teste"""
    result = {
        "module": module,
        "test": test_name,
        "status": status,
        "latency_ms": round(latency * 1000, 2),
        "details": details,
        "timestamp": datetime.now().isoformat()
    }
    results["tests"].append(result)
    results["summary"]["total"] += 1
    
    if status == "✅ PASS":
        results["summary"]["passed"] += 1
        print(f"✅ {module} - {test_name}: PASS ({result['latency_ms']}ms)")
    elif status == "❌ FAIL":
        results["summary"]["failed"] += 1
        print(f"❌ {module} - {test_name}: FAIL - {details}")
    elif status == "⚠️ WARN":
        results["summary"]["warnings"] += 1
        print(f"⚠️ {module} - {test_name}: WARN - {details}")
    
    # Atualiza latência média por módulo
    if module not in results["latency"]:
        results["latency"][module] = []
    results["latency"][module].append(latency * 1000)

def test_endpoint(method: str, endpoint: str, expected_status: int, 
                  headers: Dict = None, data: Dict = None, 
                  test_name: str = "", module: str = "API"):
    """Testa um endpoint da API"""
    url = f"{API_URL}{endpoint}"
    start_time = time.time()
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=10)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=data, timeout=10)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=10)
        
        latency = time.time() - start_time
        
        if response.status_code == expected_status:
            log_test(module, test_name or f"{method} {endpoint}", "✅ PASS", latency, 
                    f"Status {response.status_code}")
            return response
        else:
            log_test(module, test_name or f"{method} {endpoint}", "❌ FAIL", latency,
                    f"Expected {expected_status}, got {response.status_code}")
            return None
            
    except Exception as e:
        latency = time.time() - start_time
        log_test(module, test_name or f"{method} {endpoint}", "❌ FAIL", latency, str(e))
        return None

# ============================================================================
# 1. TESTES DE BACKEND API
# ============================================================================

print("\n" + "="*80)
print("1. TESTANDO BACKEND API")
print("="*80 + "\n")

# 1.1 Health Check
test_endpoint("GET", "/health", 200, test_name="Health Check", module="Backend")

# 1.2 Registro de Usuário
test_user_email = f"qa_test_{int(time.time())}@test.com"
test_user_password = "TestPassword123!"

response = test_endpoint(
    "POST", "/auth/register", 201,
    data={"email": test_user_email, "password": test_user_password},
    test_name="Registro de Usuário", module="Auth"
)

if response:
    try:
        auth_token = response.json().get("token")
        user_id = response.json().get("user", {}).get("id")
        print(f"   Token obtido: {auth_token[:20]}...")
        print(f"   User ID: {user_id}")
    except:
        auth_token = None
        user_id = None
else:
    auth_token = None
    user_id = None

# 1.3 Login
response = test_endpoint(
    "POST", "/auth/login", 200,
    data={"email": test_user_email, "password": test_user_password},
    test_name="Login de Usuário", module="Auth"
)

# 1.4 Login com Credenciais Inválidas
test_endpoint(
    "POST", "/auth/login", 401,
    data={"email": test_user_email, "password": "wrong_password"},
    test_name="Login Inválido (deve falhar)", module="Auth"
)

# 1.5 Acesso sem Autenticação
test_endpoint(
    "GET", "/kyc/status", 401,
    test_name="Acesso sem Token (deve falhar)", module="Auth"
)

# 1.6 Acesso com Token Inválido
test_endpoint(
    "GET", "/kyc/status", 401,
    headers={"Authorization": "Bearer invalid_token_123"},
    test_name="Token Inválido (deve falhar)", module="Auth"
)

# ============================================================================
# 2. TESTES DE KYC (SUMSUB)
# ============================================================================

print("\n" + "="*80)
print("2. TESTANDO INTEGRAÇÃO KYC (SUMSUB)")
print("="*80 + "\n")

if auth_token:
    headers_auth = {"Authorization": f"Bearer {auth_token}"}
    
    # 2.1 Inicializar KYC
    response = test_endpoint(
        "POST", "/kyc/init", 200,
        headers=headers_auth,
        test_name="Inicializar KYC", module="KYC"
    )
    
    access_token = None
    applicant_id = None
    
    if response:
        try:
            kyc_data = response.json()
            access_token = kyc_data.get("accessToken")
            applicant_id = kyc_data.get("applicantId")
            print(f"   Access Token: {access_token[:20] if access_token else 'N/A'}...")
            print(f"   Applicant ID: {applicant_id}")
        except:
            pass
    
    # 2.2 Consultar Status KYC
    test_endpoint(
        "GET", "/kyc/status", 200,
        headers=headers_auth,
        test_name="Consultar Status KYC", module="KYC"
    )
    
    # 2.3 Consultar Liveness Status
    test_endpoint(
        "GET", "/kyc/liveness", 200,
        headers=headers_auth,
        test_name="Consultar Liveness Status", module="KYC"
    )
    
    # 2.4 Simular Webhook do Sumsub
    webhook_payload = {
        "type": "applicantReviewed",
        "applicantId": applicant_id if applicant_id else "test-123",
        "externalUserId": str(user_id) if user_id else "1",
        "reviewStatus": "completed",
        "reviewResult": {
            "reviewAnswer": "GREEN"
        }
    }
    
    # Gerar assinatura HMAC
    payload_str = json.dumps(webhook_payload)
    signature = hmac.new(
        SUMSUB_SECRET.encode(),
        payload_str.encode(),
        hashlib.sha256
    ).hexdigest()
    
    test_endpoint(
        "POST", "/kyc/webhook", 200,
        headers={"X-Payload-Digest": f"sha256={signature}"},
        data=webhook_payload,
        test_name="Webhook Sumsub (simulado)", module="KYC"
    )
    
    # 2.5 Webhook sem Assinatura (deve falhar)
    test_endpoint(
        "POST", "/kyc/webhook", 401,
        data=webhook_payload,
        test_name="Webhook sem Assinatura (deve falhar)", module="Security"
    )
    
    # 2.6 Webhook com Assinatura Inválida (deve falhar)
    test_endpoint(
        "POST", "/kyc/webhook", 401,
        headers={"X-Payload-Digest": "sha256=invalid_signature"},
        data=webhook_payload,
        test_name="Webhook com Assinatura Inválida (deve falhar)", module="Security"
    )

# ============================================================================
# 3. TESTES DE DOCUMENTOS/BLOCKCHAIN
# ============================================================================

print("\n" + "="*80)
print("3. TESTANDO REGISTRO DE DOCUMENTOS")
print("="*80 + "\n")

if auth_token:
    # 3.1 Verificar Documento (hash de teste)
    test_hash = "0x" + "a" * 64  # Hash válido de teste
    
    response = test_endpoint(
        "POST", "/proxy/verify", 200,
        headers=headers_auth,
        data={"documentHash": test_hash},
        test_name="Verificar Documento", module="Blockchain"
    )
    
    # 3.2 Registrar Assinatura (hash de teste)
    response = test_endpoint(
        "POST", "/proxy/signature", 200,
        headers=headers_auth,
        data={
            "documentHash": test_hash,
            "signer": "0x" + "1" * 40  # Endereço Ethereum válido
        },
        test_name="Registrar Assinatura", module="Blockchain"
    )
    
    # 3.3 Mint Identity (endereço de teste)
    response = test_endpoint(
        "POST", "/proxy/identity", 200,
        headers=headers_auth,
        data={
            "wallet": "0x" + "2" * 40,
            "proofCid": "Qm" + "a" * 44  # CID IPFS válido
        },
        test_name="Mint Identity", module="Blockchain"
    )

# ============================================================================
# 4. TESTES DE SEGURANÇA
# ============================================================================

print("\n" + "="*80)
print("4. TESTANDO SEGURANÇA")
print("="*80 + "\n")

# 4.1 SQL Injection
test_endpoint(
    "POST", "/auth/login", 401,
    data={"email": "admin' OR '1'='1", "password": "anything"},
    test_name="SQL Injection (deve falhar)", module="Security"
)

# 4.2 XSS
test_endpoint(
    "POST", "/auth/register", 400,
    data={"email": "<script>alert('xss')</script>@test.com", "password": "Test123!"},
    test_name="XSS no Email (deve falhar)", module="Security"
)

# 4.3 Campos Obrigatórios
test_endpoint(
    "POST", "/auth/register", 400,
    data={"email": "test@test.com"},  # Falta password
    test_name="Registro sem Senha (deve falhar)", module="Security"
)

test_endpoint(
    "POST", "/auth/login", 400,
    data={"password": "test123"},  # Falta email
    test_name="Login sem Email (deve falhar)", module="Security"
)

# ============================================================================
# 5. TESTES DE FRONTEND
# ============================================================================

print("\n" + "="*80)
print("5. TESTANDO FRONTEND")
print("="*80 + "\n")

# 5.1 Página Inicial
start_time = time.time()
try:
    response = requests.get(BASE_URL, timeout=10)
    latency = time.time() - start_time
    
    if response.status_code == 200 and "BTS Blocktrust" in response.text:
        log_test("Frontend", "Página Inicial", "✅ PASS", latency, "HTML carregado")
    else:
        log_test("Frontend", "Página Inicial", "❌ FAIL", latency, "Conteúdo inválido")
except Exception as e:
    latency = time.time() - start_time
    log_test("Frontend", "Página Inicial", "❌ FAIL", latency, str(e))

# 5.2 Assets Estáticos
for asset in ["/assets/index.css", "/assets/index.js"]:
    start_time = time.time()
    try:
        response = requests.get(f"{BASE_URL}{asset}", timeout=10)
        latency = time.time() - start_time
        
        if response.status_code == 200:
            log_test("Frontend", f"Asset {asset}", "✅ PASS", latency, "Carregado")
        else:
            log_test("Frontend", f"Asset {asset}", "⚠️ WARN", latency, f"Status {response.status_code}")
    except Exception as e:
        latency = time.time() - start_time
        log_test("Frontend", f"Asset {asset}", "⚠️ WARN", latency, str(e))

# 5.3 Logo
start_time = time.time()
try:
    response = requests.get(f"{BASE_URL}/blocktrust.png", timeout=10)
    latency = time.time() - start_time
    
    if response.status_code == 200:
        log_test("Frontend", "Logo", "✅ PASS", latency, "Imagem carregada")
    else:
        log_test("Frontend", "Logo", "⚠️ WARN", latency, f"Status {response.status_code}")
except Exception as e:
    latency = time.time() - start_time
    log_test("Frontend", "Logo", "⚠️ WARN", latency, str(e))

# ============================================================================
# 6. RELATÓRIO FINAL
# ============================================================================

print("\n" + "="*80)
print("RELATÓRIO FINAL")
print("="*80 + "\n")

# Calcular latências médias por módulo
print("Latência Média por Módulo:")
print("-" * 50)
for module, latencies in results["latency"].items():
    avg_latency = sum(latencies) / len(latencies)
    status = "✅" if avg_latency < 500 else "⚠️"
    print(f"{status} {module:20s}: {avg_latency:6.2f}ms")

print("\n" + "-" * 50)
print(f"Total de Testes: {results['summary']['total']}")
print(f"✅ Passaram:     {results['summary']['passed']}")
print(f"❌ Falharam:     {results['summary']['failed']}")
print(f"⚠️  Avisos:       {results['summary']['warnings']}")

# Taxa de sucesso
success_rate = (results['summary']['passed'] / results['summary']['total']) * 100
print(f"\n📊 Taxa de Sucesso: {success_rate:.1f}%")

# Status final
if results['summary']['failed'] == 0:
    print("\n✅ TODOS OS TESTES CRÍTICOS PASSARAM!")
    print("🎉 Aplicação aprovada para produção!")
else:
    print(f"\n❌ {results['summary']['failed']} TESTES FALHARAM")
    print("⚠️  Revisar falhas antes de aprovar para produção")

# Salvar relatório JSON
os.makedirs("/home/ubuntu/bts-blocktrust/qa/reports", exist_ok=True)
report_path = "/home/ubuntu/bts-blocktrust/qa/reports/blocktrust-qa-report.json"

with open(report_path, "w") as f:
    json.dump(results, f, indent=2)

print(f"\n📄 Relatório salvo em: {report_path}")

# Criar relatório Markdown
md_report = f"""# Relatório de QA - BTS Blocktrust

**Data:** {results['timestamp']}

## Resumo Executivo

- **Total de Testes:** {results['summary']['total']}
- **✅ Passaram:** {results['summary']['passed']}
- **❌ Falharam:** {results['summary']['failed']}
- **⚠️ Avisos:** {results['summary']['warnings']}
- **Taxa de Sucesso:** {success_rate:.1f}%

## Latência Média por Módulo

| Módulo | Latência Média | Status |
|--------|----------------|--------|
"""

for module, latencies in results["latency"].items():
    avg_latency = sum(latencies) / len(latencies)
    status = "✅ OK" if avg_latency < 500 else "⚠️ Alto"
    md_report += f"| {module} | {avg_latency:.2f}ms | {status} |\n"

md_report += "\n## Detalhes dos Testes\n\n"

for test in results["tests"]:
    md_report += f"### {test['module']} - {test['test']}\n\n"
    md_report += f"- **Status:** {test['status']}\n"
    md_report += f"- **Latência:** {test['latency_ms']}ms\n"
    if test['details']:
        md_report += f"- **Detalhes:** {test['details']}\n"
    md_report += "\n"

md_report_path = "/home/ubuntu/bts-blocktrust/qa/reports/blocktrust-qa-report.md"
with open(md_report_path, "w") as f:
    f.write(md_report)

print(f"📄 Relatório Markdown salvo em: {md_report_path}")
print("\n" + "="*80)

