#!/usr/bin/env python3
"""
Script de Validação Completa dos Fluxos do Blocktrust v1.4
Valida todos os fluxos implementados, incluindo jornada failsafe
"""

import requests
import json
import hashlib
import time
from datetime import datetime

# Configurações
BASE_URL = "https://bts-blocktrust.onrender.com"  # Produção
# BASE_URL = "http://localhost:10000"  # Local

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(80)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")

# Variáveis globais para armazenar dados do teste
test_data = {
    'email': f'test_{int(time.time())}@blocktrust.test',
    'password': 'TestNormal123!',
    'coercion_password': 'TestCoercion456!',
    'token': None,
    'user_id': None,
    'nft_id': None,
    'wallet_address': None
}

def validate_health():
    """Valida health check da API"""
    print_header("1. VALIDAÇÃO DE HEALTH CHECK")
    
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"API está online: {data}")
            return True
        else:
            print_error(f"API retornou status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Erro ao conectar à API: {str(e)}")
        return False

def validate_register_with_two_passwords():
    """Valida cadastro com duas senhas (normal e de coação)"""
    print_header("2. VALIDAÇÃO DE CADASTRO COM DUAS SENHAS")
    
    try:
        # Teste 1: Cadastro completo
        print_info("Teste 1: Cadastro com senha normal e senha de coação")
        response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json={
                'email': test_data['email'],
                'password': test_data['password'],
                'coercion_password': test_data['coercion_password']
            },
            timeout=10
        )
        
        if response.status_code == 201:
            data = response.json()
            test_data['token'] = data['token']
            test_data['user_id'] = data['user']['id']
            print_success(f"Usuário cadastrado: {data['user']['email']}")
            print_success(f"Token recebido: {test_data['token'][:20]}...")
            print_success(f"User ID: {test_data['user_id']}")
        else:
            print_error(f"Erro no cadastro: {response.text}")
            return False
        
        # Teste 2: Verificar se failsafe está configurado
        print_info("\nTeste 2: Verificar se failsafe foi configurado automaticamente")
        response = requests.get(
            f"{BASE_URL}/api/failsafe/status",
            headers={'Authorization': f'Bearer {test_data["token"]}'},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('failsafe_configured'):
                print_success("Failsafe configurado automaticamente no cadastro")
            else:
                print_error("Failsafe NÃO foi configurado automaticamente")
                return False
        else:
            print_error(f"Erro ao verificar status do failsafe: {response.text}")
            return False
        
        # Teste 3: Tentar cadastrar com senhas iguais (deve falhar)
        print_info("\nTeste 3: Validação - senhas iguais devem ser rejeitadas")
        response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json={
                'email': f'test_fail_{int(time.time())}@blocktrust.test',
                'password': 'SamePwd123!',
                'coercion_password': 'SamePwd123!'
            },
            timeout=10
        )
        
        if response.status_code == 400:
            print_success("Validação OK: Senhas iguais foram rejeitadas")
        else:
            print_error("Validação FALHOU: Senhas iguais foram aceitas")
            return False
        
        return True
        
    except Exception as e:
        print_error(f"Erro na validação de cadastro: {str(e)}")
        return False

def validate_wallet_creation():
    """Valida criação automática de carteira"""
    print_header("3. VALIDAÇÃO DE CRIAÇÃO DE CARTEIRA")
    
    try:
        print_info("Inicializando carteira...")
        response = requests.post(
            f"{BASE_URL}/api/wallet/init",
            json={'password': test_data['password']},
            headers={'Authorization': f'Bearer {test_data["token"]}'},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            test_data['wallet_address'] = data['address']
            print_success(f"Carteira criada: {test_data['wallet_address']}")
            return True
        else:
            print_error(f"Erro ao criar carteira: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Erro na validação de carteira: {str(e)}")
        return False

def validate_kyc_to_nft_flow():
    """Valida fluxo KYC → NFT"""
    print_header("4. VALIDAÇÃO DO FLUXO KYC → NFT")
    
    try:
        # Simular aprovação de KYC (em produção, isso viria do Sumsub)
        print_info("Simulando aprovação de KYC...")
        print_warning("⚠️  Em produção, isso seria feito pelo webhook do Sumsub")
        
        # Verificar status do NFT
        print_info("\nVerificando status do NFT...")
        response = requests.get(
            f"{BASE_URL}/api/nft/status",
            headers={'Authorization': f'Bearer {test_data["token"]}'},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print_info(f"Status do NFT: {json.dumps(data, indent=2)}")
            
            if data.get('nft_id'):
                test_data['nft_id'] = data['nft_id']
                print_success(f"NFT encontrado: ID={test_data['nft_id']}")
            else:
                print_warning("NFT ainda não foi mintado (aguardando KYC)")
            
            return True
        else:
            print_error(f"Erro ao verificar NFT: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Erro na validação de KYC→NFT: {str(e)}")
        return False

def validate_normal_signature():
    """Valida assinatura normal (com senha normal)"""
    print_header("5. VALIDAÇÃO DE ASSINATURA NORMAL")
    
    try:
        # Gerar hash de documento de teste
        doc_content = f"Documento de teste - {datetime.now().isoformat()}"
        doc_hash = "0x" + hashlib.sha256(doc_content.encode()).hexdigest()
        
        print_info(f"Hash do documento: {doc_hash}")
        print_info("Assinando com SENHA NORMAL...")
        
        response = requests.post(
            f"{BASE_URL}/api/signature/sign-document",
            json={
                'file_hash': doc_hash,
                'password': test_data['password'],  # Senha NORMAL
                'document_name': 'documento_teste.pdf'
            },
            headers={'Authorization': f'Bearer {test_data["token"]}'},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('failsafe_triggered'):
                print_error("ERRO: Failsafe foi acionado com senha NORMAL!")
                return False
            
            print_success("Documento assinado com sucesso (modo normal)")
            print_success(f"Assinatura: {data.get('signature', 'N/A')[:50]}...")
            
            if data.get('blockchain_tx'):
                print_success(f"Registrado na blockchain: {data['blockchain_tx']}")
            
            return True
        else:
            print_error(f"Erro ao assinar documento: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Erro na validação de assinatura normal: {str(e)}")
        return False

def validate_failsafe_signature():
    """Valida assinatura failsafe (com senha de coação)"""
    print_header("6. VALIDAÇÃO DE ASSINATURA FAILSAFE (COAÇÃO)")
    
    try:
        # Gerar hash de documento de teste
        doc_content = f"Documento COAGIDO - {datetime.now().isoformat()}"
        doc_hash = "0x" + hashlib.sha256(doc_content.encode()).hexdigest()
        
        print_info(f"Hash do documento: {doc_hash}")
        print_warning("🚨 Assinando com SENHA DE COAÇÃO (FAILSAFE)...")
        
        response = requests.post(
            f"{BASE_URL}/api/signature/sign-document",
            json={
                'file_hash': doc_hash,
                'password': test_data['coercion_password'],  # Senha de COAÇÃO
                'document_name': 'documento_coagido.pdf'
            },
            headers={'Authorization': f'Bearer {test_data["token"]}'},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # VALIDAÇÕES CRÍTICAS DO FAILSAFE
            checks = []
            
            # 1. Failsafe deve ter sido acionado
            if data.get('failsafe_triggered') or data.get('status') == 'failsafe':
                print_success("✓ Failsafe foi acionado corretamente")
                checks.append(True)
            else:
                print_error("✗ Failsafe NÃO foi acionado com senha de coação!")
                checks.append(False)
            
            # 2. NFT deve ter sido cancelado
            if data.get('nft_cancelled'):
                print_success("✓ NFT foi cancelado automaticamente")
                checks.append(True)
            else:
                print_warning("✗ NFT NÃO foi cancelado")
                checks.append(False)
            
            # 3. Assinatura deve ser fake (não deve ter tx blockchain)
            if not data.get('blockchain_tx'):
                print_success("✓ Assinatura fake (sem registro blockchain)")
                checks.append(True)
            else:
                print_error("✗ Assinatura foi registrada na blockchain (deveria ser fake!)")
                checks.append(False)
            
            # 4. Deve ter mensagem de emergência
            if 'EMERGÊNCIA' in data.get('message', '').upper() or 'FAILSAFE' in data.get('message', '').upper():
                print_success("✓ Mensagem de emergência presente")
                checks.append(True)
            else:
                print_warning("✗ Mensagem de emergência não encontrada")
                checks.append(False)
            
            print(f"\n{Colors.BOLD}Resultado: {sum(checks)}/{len(checks)} validações passaram{Colors.END}")
            
            return all(checks)
        else:
            print_error(f"Erro ao assinar documento: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Erro na validação de failsafe: {str(e)}")
        return False

def validate_failsafe_status_after():
    """Valida status do failsafe após acionamento"""
    print_header("7. VALIDAÇÃO DE STATUS PÓS-FAILSAFE")
    
    try:
        print_info("Verificando status do failsafe após acionamento...")
        response = requests.get(
            f"{BASE_URL}/api/failsafe/status",
            headers={'Authorization': f'Bearer {test_data["token"]}'},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('last_trigger'):
                print_success(f"Último acionamento registrado: {data['last_trigger']}")
            else:
                print_warning("Último acionamento não foi registrado")
            
            # Verificar se NFT está inativo
            print_info("\nVerificando status do NFT após failsafe...")
            response = requests.get(
                f"{BASE_URL}/api/nft/status",
                headers={'Authorization': f'Bearer {test_data["token"]}'},
                timeout=10
            )
            
            if response.status_code == 200:
                nft_data = response.json()
                
                if not nft_data.get('nft_active'):
                    print_success("✓ NFT está INATIVO após failsafe")
                    return True
                else:
                    print_error("✗ NFT ainda está ATIVO após failsafe!")
                    return False
            else:
                print_error(f"Erro ao verificar NFT: {response.text}")
                return False
        else:
            print_error(f"Erro ao verificar status: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Erro na validação pós-failsafe: {str(e)}")
        return False

def main():
    """Executa todas as validações"""
    print_header("VALIDAÇÃO COMPLETA DOS FLUXOS - BLOCKTRUST V1.4")
    print(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"URL: {BASE_URL}")
    
    results = {}
    
    # Executar validações
    results['health'] = validate_health()
    
    if results['health']:
        results['register'] = validate_register_with_two_passwords()
        
        if results['register']:
            results['wallet'] = validate_wallet_creation()
            results['kyc_nft'] = validate_kyc_to_nft_flow()
            results['normal_signature'] = validate_normal_signature()
            results['failsafe_signature'] = validate_failsafe_signature()
            results['failsafe_status'] = validate_failsafe_status_after()
    
    # Resumo final
    print_header("RESUMO DA VALIDAÇÃO")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for test, result in results.items():
        status = f"{Colors.GREEN}✅ PASSOU{Colors.END}" if result else f"{Colors.RED}❌ FALHOU{Colors.END}"
        print(f"{test.upper().replace('_', ' ')}: {status}")
    
    print(f"\n{Colors.BOLD}RESULTADO FINAL: {passed}/{total} testes passaram{Colors.END}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 TODOS OS FLUXOS ESTÃO FUNCIONANDO CORRETAMENTE!{Colors.END}")
        return 0
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}⚠️  ALGUNS FLUXOS FALHARAM - REVISÃO NECESSÁRIA{Colors.END}")
        return 1

if __name__ == '__main__':
    exit(main())

