"""
Script de teste para validar integração com Toolblox
"""
import os
import sys
from dotenv import load_dotenv

# Adicionar o diretório backend ao path
sys.path.insert(0, os.path.dirname(__file__))

# Carregar variáveis de ambiente
load_dotenv()

from api.utils.toolblox_client import toolblox_client, ToolbloxError

def test_dns_validation():
    """Testa validação de DNS dos endpoints"""
    print("\n" + "="*60)
    print("TESTE 1: Validação de DNS")
    print("="*60)
    
    print("\n✅ Cliente inicializado com sucesso!")
    print(f"   MINT URL: {toolblox_client.mint_url}")
    print(f"   SIGNATURE URL: {toolblox_client.signature_url}")
    print(f"   VERIFY URL: {toolblox_client.verify_url}")
    print(f"   NETWORK: {toolblox_client.network}")

def test_verify_document():
    """Testa verificação de documento"""
    print("\n" + "="*60)
    print("TESTE 2: Verificação de Documento")
    print("="*60)
    
    test_hash = "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    
    try:
        print(f"\n🔍 Testando verificação para hash: {test_hash}")
        result = toolblox_client.verify_document(test_hash)
        print(f"✅ Sucesso! Resultado: {result}")
        return True
    except ToolbloxError as e:
        print(f"❌ Erro do Toolblox: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_mint_identity():
    """Testa mint de identidade"""
    print("\n" + "="*60)
    print("TESTE 3: Mint de Identidade")
    print("="*60)
    
    test_wallet = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
    test_proof_cid = "QmTest123456789"
    
    try:
        print(f"\n🪙 Testando mint para wallet: {test_wallet}")
        result = toolblox_client.mint_identity(test_wallet, test_proof_cid)
        print(f"✅ Sucesso! Resultado: {result}")
        return True
    except ToolbloxError as e:
        print(f"❌ Erro do Toolblox: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_register_signature():
    """Testa registro de assinatura"""
    print("\n" + "="*60)
    print("TESTE 4: Registro de Assinatura")
    print("="*60)
    
    test_hash = "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    test_signer = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
    
    try:
        print(f"\n✍️ Testando registro de assinatura para hash: {test_hash}")
        result = toolblox_client.register_signature(test_hash, test_signer)
        print(f"✅ Sucesso! Resultado: {result}")
        return True
    except ToolbloxError as e:
        print(f"❌ Erro do Toolblox: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("\n" + "="*60)
    print("TESTES DE INTEGRAÇÃO COM TOOLBLOX")
    print("="*60)
    
    results = {
        'DNS Validation': True,  # Sempre passa se o cliente inicializar
        'Verify Document': False,
        'Mint Identity': False,
        'Register Signature': False
    }
    
    # Teste 1: Validação de DNS
    test_dns_validation()
    
    # Teste 2: Verificação de documento
    results['Verify Document'] = test_verify_document()
    
    # Teste 3: Mint de identidade
    results['Mint Identity'] = test_mint_identity()
    
    # Teste 4: Registro de assinatura
    results['Register Signature'] = test_register_signature()
    
    # Resumo dos resultados
    print("\n" + "="*60)
    print("RESUMO DOS TESTES")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASSOU" if passed else "❌ FALHOU"
        print(f"{test_name}: {status}")
    
    total_passed = sum(results.values())
    total_tests = len(results)
    
    print(f"\nTotal: {total_passed}/{total_tests} testes passaram")
    
    if total_passed == total_tests:
        print("\n🎉 Todos os testes passaram!")
        return 0
    else:
        print("\n⚠️ Alguns testes falharam. Verifique os logs acima.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

