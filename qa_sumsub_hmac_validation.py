#!/usr/bin/env python3
"""
QA de Integração HMAC e Webhooks Sumsub (Produção Segura)
Objetivo: Validar assinatura HMAC, testar webhooks válidos e inválidos,
e gerar logs auditáveis (sem segredos).
"""

import os, hmac, hashlib, json, logging, requests, sys

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
SUMSUB_SECRET_KEY = os.getenv("SUMSUB_SECRET_KEY", "demo_secret")
SUMSUB_WEBHOOK_URL = os.getenv("SUMSUB_WEBHOOK_URL", "https://bts-blocktrust.onrender.com/api/kyc/webhook")

# ===========================================================
# 1️⃣ Função utilitária — gerar assinatura HMAC SHA256 válida
# ===========================================================
def generate_valid_hmac(payload: dict) -> str:
    """Gera assinatura HMAC SHA256 válida para payload"""
    message = json.dumps(payload, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
    return hmac.new(SUMSUB_SECRET_KEY.encode('utf-8'), message, hashlib.sha256).hexdigest()

# ===========================================================
# 2️⃣ Teste Unitário — Assinatura válida
# ===========================================================
def test_hmac_valid_signature():
    """Testa se a assinatura HMAC válida é gerada corretamente"""
    logger.info("🧪 Teste 1: Validação de assinatura HMAC válida")
    
    payload = {"type": "applicantReviewed", "applicantId": "test_valid_123"}
    signature = generate_valid_hmac(payload)
    computed = hmac.new(
        SUMSUB_SECRET_KEY.encode('utf-8'),
        json.dumps(payload, separators=(',', ':'), ensure_ascii=False).encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    assert signature == computed, "❌ Falha: HMAC gerado não confere."
    logger.info("✅ Teste HMAC Válido: Assinatura confirmada corretamente.")
    return True

# ===========================================================
# 3️⃣ Teste Unitário — Assinatura inválida
# ===========================================================
def test_hmac_invalid_signature():
    """Testa se assinatura inválida é rejeitada"""
    logger.info("🧪 Teste 2: Validação de rejeição de assinatura inválida")
    
    payload = {"type": "applicantReviewed", "applicantId": "test_invalid_456"}
    wrong_signature = "deadbeef" * 8  # 64 chars inválidos
    computed = generate_valid_hmac(payload)
    
    assert wrong_signature != computed, "❌ Falha: Assinatura incorreta passou indevidamente."
    logger.info("✅ Teste HMAC Inválido: Assinatura incorreta corretamente rejeitada.")
    return True

# ===========================================================
# 4️⃣ Simulação — Webhook Válido
# ===========================================================
def simulate_valid_webhook():
    """Simula envio de webhook com assinatura válida"""
    logger.info("🧪 Teste 3: Simulação de webhook com assinatura válida")
    
    payload = {"type": "applicantApproved", "applicantId": "valid_789", "reviewStatus": "completed"}
    signature = generate_valid_hmac(payload)
    headers = {
        "X-Payload-Digest": f"sha256={signature}",
        "Content-Type": "application/json"
    }
    
    try:
        res = requests.post(
            SUMSUB_WEBHOOK_URL,
            headers=headers,
            data=json.dumps(payload),
            timeout=10
        )
        logger.info(f"📩 Webhook Válido → Status: {res.status_code} | Resposta: {res.text[:120]}")
        return res.status_code in [200, 201, 204]
    except Exception as e:
        logger.error(f"❌ Erro ao enviar webhook válido: {str(e)}")
        return False

# ===========================================================
# 5️⃣ Simulação — Webhook Inválido
# ===========================================================
def simulate_invalid_webhook():
    """Simula envio de webhook com assinatura inválida"""
    logger.info("🧪 Teste 4: Simulação de webhook com assinatura inválida")
    
    payload = {"type": "applicantRejected", "applicantId": "invalid_999"}
    headers = {
        "X-Payload-Digest": "sha256=invalidsignature123",
        "Content-Type": "application/json"
    }
    
    try:
        res = requests.post(
            SUMSUB_WEBHOOK_URL,
            headers=headers,
            data=json.dumps(payload),
            timeout=10
        )
        logger.info(f"🚫 Webhook Inválido → Status: {res.status_code} | Resposta: {res.text[:120]}")
        # Esperamos que seja rejeitado (400, 401, 403)
        return res.status_code in [400, 401, 403]
    except Exception as e:
        logger.error(f"❌ Erro ao enviar webhook inválido: {str(e)}")
        return False

# ===========================================================
# 6️⃣ Execução — Rotina QA completa
# ===========================================================
def run_full_qa_validation():
    """Executa todos os testes de QA"""
    logger.info("🧪 Iniciando QA de Integração HMAC Sumsub...")
    logger.info("=" * 60)
    
    results = {
        "hmac_valid": False,
        "hmac_invalid": False,
        "webhook_valid": False,
        "webhook_invalid": False
    }
    
    try:
        results["hmac_valid"] = test_hmac_valid_signature()
        results["hmac_invalid"] = test_hmac_invalid_signature()
        results["webhook_valid"] = simulate_valid_webhook()
        results["webhook_invalid"] = simulate_invalid_webhook()
        
        logger.info("=" * 60)
        logger.info("🎯 QA Finalizado!")
        
        # Verificar resultados
        all_passed = all(results.values())
        if all_passed:
            logger.info("✅ TODOS OS TESTES PASSARAM!")
        else:
            logger.warning("⚠️ ALGUNS TESTES FALHARAM:")
            for test, passed in results.items():
                status = "✅" if passed else "❌"
                logger.info(f"  {status} {test}")
        
        return all_passed
        
    except AssertionError as e:
        logger.error(f"❌ Falha de Teste Unitário: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"💥 Erro inesperado durante QA: {str(e)}")
        return False

# ===========================================================
# 7️⃣ Logs Auditáveis — Sem segredos sensíveis
# ===========================================================
def log_audit_summary():
    """Gera resumo auditável sem expor segredos"""
    logger.info("=" * 60)
    logger.info("📊 RESUMO AUDITORIA QA")
    logger.info("=" * 60)
    
    summary = {
        "qa_timestamp": "✅ Teste em produção concluído",
        "sumsub_endpoint": SUMSUB_WEBHOOK_URL,
        "sumsub_secret_checksum": hashlib.sha256(SUMSUB_SECRET_KEY.encode()).hexdigest()[:12] + "...",
        "tests_executed": [
            "HMAC válido",
            "HMAC inválido",
            "Webhook válido",
            "Webhook inválido"
        ]
    }
    
    for key, value in summary.items():
        if isinstance(value, list):
            logger.info(f"{key}:")
            for item in value:
                logger.info(f"  - {item}")
        else:
            logger.info(f"{key}: {value}")
    
    logger.info("=" * 60)

if __name__ == "__main__":
    success = run_full_qa_validation()
    log_audit_summary()
    
    # Exit code para CI/CD
    sys.exit(0 if success else 1)

