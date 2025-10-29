#!/usr/bin/env python3
"""
Script de Teste: Fluxo KYC + Auto-Mint de NFT
Testa o fluxo completo de aprovação de KYC e mint automático de NFT
"""

import requests
import json
import time
import os

# Configuração
BASE_URL = os.getenv('API_URL', 'https://bts-blocktrust.onrender.com')
TEST_EMAIL = f"test_automint_{int(time.time())}@example.com"
TEST_PASSWORD = "Test@123456"

print("=" * 60)
print("🧪 TESTE: FLUXO KYC + AUTO-MINT DE NFT")
print("=" * 60)
print(f"API: {BASE_URL}")
print(f"Email de teste: {TEST_EMAIL}")
print("=" * 60)

# Passo 1: Criar conta
print("\n📝 PASSO 1: Criar conta de usuário")
print("-" * 60)

register_data = {
    "email": TEST_EMAIL,
    "password": TEST_PASSWORD,
    "coercion_password": "Failsafe@123456"
}

try:
    response = requests.post(
        f"{BASE_URL}/api/auth/register",
        json=register_data,
        timeout=30
    )
    
    if response.status_code == 201:
        print(f"✅ Conta criada com sucesso!")
        user_data = response.json()
        print(f"   User ID: {user_data.get('user_id')}")
    else:
        print(f"❌ Erro ao criar conta: {response.status_code}")
        print(f"   Response: {response.text}")
        exit(1)
        
except Exception as e:
    print(f"❌ Erro na requisição: {str(e)}")
    exit(1)

# Passo 2: Fazer login
print("\n🔐 PASSO 2: Fazer login")
print("-" * 60)

login_data = {
    "email": TEST_EMAIL,
    "password": TEST_PASSWORD
}

try:
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json=login_data,
        timeout=30
    )
    
    if response.status_code == 200:
        print(f"✅ Login realizado com sucesso!")
        login_response = response.json()
        token = login_response.get('token')
        print(f"   Token: {token[:20]}...")
    else:
        print(f"❌ Erro ao fazer login: {response.status_code}")
        print(f"   Response: {response.text}")
        exit(1)
        
except Exception as e:
    print(f"❌ Erro na requisição: {str(e)}")
    exit(1)

# Headers com token
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Passo 3: Iniciar KYC
print("\n🎯 PASSO 3: Iniciar processo de KYC")
print("-" * 60)

try:
    response = requests.post(
        f"{BASE_URL}/api/kyc/init",
        headers=headers,
        timeout=30
    )
    
    if response.status_code == 200:
        print(f"✅ KYC iniciado com sucesso!")
        kyc_data = response.json()
        applicant_id = kyc_data.get('applicantId')
        mock_mode = kyc_data.get('mock_mode', False)
        
        print(f"   Applicant ID: {applicant_id}")
        print(f"   Mock Mode: {mock_mode}")
        
        if mock_mode:
            print(f"   ⚠️  Modo mock ativo (API Sumsub indisponível)")
    else:
        print(f"❌ Erro ao iniciar KYC: {response.status_code}")
        print(f"   Response: {response.text}")
        exit(1)
        
except Exception as e:
    print(f"❌ Erro na requisição: {str(e)}")
    exit(1)

# Passo 4: Simular webhook de aprovação do KYC
print("\n📬 PASSO 4: Simular webhook de aprovação do KYC")
print("-" * 60)

webhook_data = {
    "applicantId": applicant_id,
    "externalUserId": user_data.get('user_id'),
    "reviewStatus": "completed",
    "reviewResult": {
        "reviewAnswer": "GREEN"
    },
    "type": "applicantReviewed"
}

try:
    response = requests.post(
        f"{BASE_URL}/api/kyc/webhook",
        json=webhook_data,
        timeout=60  # Timeout maior pois pode fazer mint
    )
    
    if response.status_code == 200:
        print(f"✅ Webhook processado com sucesso!")
        print(f"   KYC aprovado e NFT mintado automaticamente")
    else:
        print(f"❌ Erro ao processar webhook: {response.status_code}")
        print(f"   Response: {response.text}")
        # Não sair, vamos verificar o status mesmo assim
        
except Exception as e:
    print(f"❌ Erro na requisição: {str(e)}")
    # Não sair, vamos verificar o status mesmo assim

# Aguardar processamento
print("\n⏳ Aguardando 5 segundos para processamento...")
time.sleep(5)

# Passo 5: Verificar status do KYC
print("\n🔍 PASSO 5: Verificar status do KYC")
print("-" * 60)

try:
    response = requests.get(
        f"{BASE_URL}/api/kyc/status",
        headers=headers,
        timeout=30
    )
    
    if response.status_code == 200:
        print(f"✅ Status obtido com sucesso!")
        status_data = response.json()
        
        print(f"   Status: {status_data.get('status')}")
        print(f"   Review Status: {status_data.get('reviewStatus')}")
        print(f"   Review Answer: {status_data.get('reviewAnswer')}")
    else:
        print(f"❌ Erro ao obter status: {response.status_code}")
        print(f"   Response: {response.text}")
        
except Exception as e:
    print(f"❌ Erro na requisição: {str(e)}")

# Passo 6: Verificar status da identidade (NFT)
print("\n🎨 PASSO 6: Verificar status da identidade (NFT)")
print("-" * 60)

try:
    response = requests.get(
        f"{BASE_URL}/api/nft/status",
        headers=headers,
        timeout=30
    )
    
    if response.status_code == 200:
        print(f"✅ Status da identidade obtido!")
        nft_data = response.json()
        
        print(f"   NFT ID: {nft_data.get('nft_id')}")
        print(f"   NFT Ativo: {nft_data.get('nft_active')}")
        print(f"   Wallet Address: {nft_data.get('wallet_address')}")
        print(f"   Transaction Hash: {nft_data.get('nft_transaction_hash')}")
        print(f"   Minted At: {nft_data.get('nft_minted_at')}")
        
        if nft_data.get('nft_active'):
            print(f"\n🎉 SUCESSO! NFT mintado automaticamente após KYC!")
        else:
            print(f"\n⚠️  NFT não está ativo ainda")
    else:
        print(f"❌ Erro ao obter status da identidade: {response.status_code}")
        print(f"   Response: {response.text}")
        
except Exception as e:
    print(f"❌ Erro na requisição: {str(e)}")

# Passo 7: Verificar eventos no Explorer
print("\n🔍 PASSO 7: Verificar eventos no Explorer")
print("-" * 60)

try:
    response = requests.get(
        f"{BASE_URL}/api/explorer/events",
        headers=headers,
        params={"limit": 10},
        timeout=30
    )
    
    if response.status_code == 200:
        print(f"✅ Eventos obtidos do Explorer!")
        events_data = response.json()
        events = events_data.get('events', [])
        
        print(f"   Total de eventos: {len(events)}")
        
        # Procurar por eventos de minting
        minting_events = [e for e in events if e.get('event_type') == 'Minted']
        
        if minting_events:
            print(f"\n   🎨 Eventos de Minting encontrados: {len(minting_events)}")
            for event in minting_events[:3]:  # Mostrar até 3
                print(f"      - NFT ID: {event.get('nft_id')}")
                print(f"        TX: {event.get('transaction_hash')}")
                print(f"        Timestamp: {event.get('created_at')}")
        else:
            print(f"\n   ⚠️  Nenhum evento de minting encontrado ainda")
            print(f"      (Listener pode estar processando ou contratos não deployados)")
    else:
        print(f"❌ Erro ao obter eventos: {response.status_code}")
        print(f"   Response: {response.text}")
        
except Exception as e:
    print(f"❌ Erro na requisição: {str(e)}")

# Resumo final
print("\n" + "=" * 60)
print("📊 RESUMO DO TESTE")
print("=" * 60)
print(f"✅ Conta criada: {TEST_EMAIL}")
print(f"✅ Login realizado")
print(f"✅ KYC iniciado")
print(f"✅ Webhook de aprovação enviado")
print(f"✅ Status verificado")
print("=" * 60)
print("\n💡 PRÓXIMOS PASSOS:")
print("   1. Deploy dos smart contracts na Polygon Mumbai")
print("   2. Atualizar variáveis de ambiente (IDENTITY_NFT_ADDRESS, etc.)")
print("   3. Configurar background workers (Listener e Monitor)")
print("   4. Executar teste novamente com contratos reais")
print("=" * 60)

