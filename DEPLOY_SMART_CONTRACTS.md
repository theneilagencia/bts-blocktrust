# Guia de Deploy de Smart Contracts - Blocktrust v1.4

## Visão Geral

Este guia detalha o processo completo de deploy dos smart contracts do Blocktrust na testnet Polygon Mumbai.

## Pré-requisitos

### 1. Carteira com MATIC de Teste

Você precisará de uma carteira com pelo menos **0.5 MATIC** de teste para fazer o deploy dos 3 contratos.

**Opção A: Usar Carteira Existente**
- Se você já tem uma carteira MetaMask configurada para Polygon Mumbai, use-a
- Exporte a chave privada: MetaMask → Configurações → Segurança → Exportar chave privada

**Opção B: Criar Nova Carteira (Recomendado para Produção)**
```bash
cd /home/ubuntu/bts-blocktrust
python3 -c "
from eth_account import Account
import secrets

# Gerar nova carteira
private_key = '0x' + secrets.token_hex(32)
account = Account.from_key(private_key)

print('🔐 NOVA CARTEIRA CRIADA')
print('=' * 60)
print(f'Private Key: {private_key}')
print(f'Address:     {account.address}')
print('=' * 60)
print('⚠️  IMPORTANTE: Salve a chave privada em local seguro!')
"
```

### 2. Obter MATIC de Teste

**Faucets Disponíveis:**

1. **QuickNode Faucet** (Recomendado)
   - URL: https://faucet.quicknode.com/polygon/mumbai
   - Requisito: 0.001 ETH na Ethereum Mainnet
   - Quantidade: 0.1 MATIC por drip (a cada 12h)

2. **Alchemy Faucet**
   - URL: https://mumbaifaucet.com/
   - Requisito: Conta Alchemy (gratuita)
   - Quantidade: 0.5 MATIC por dia

3. **Polygon Official Faucet**
   - URL: https://faucet.polygon.technology/
   - Requisito: Conta Google/GitHub
   - Quantidade: 0.2 MATIC por dia

**Passos para obter MATIC:**
1. Acesse um dos faucets acima
2. Cole o endereço da sua carteira
3. Complete a verificação (CAPTCHA, tweet, etc.)
4. Aguarde a transação ser confirmada (1-2 minutos)
5. Verifique o saldo em: https://mumbai.polygonscan.com/address/SEU_ENDERECO

### 3. Configurar RPC URL

**Opção A: Alchemy (Recomendado)**
1. Crie conta gratuita em: https://www.alchemy.com/
2. Crie um novo App para Polygon Mumbai
3. Copie o RPC URL (formato: `https://polygon-mumbai.g.alchemy.com/v2/YOUR_API_KEY`)

**Opção B: Infura**
1. Crie conta gratuita em: https://infura.io/
2. Crie um novo projeto para Polygon Mumbai
3. Copie o RPC URL (formato: `https://polygon-mumbai.infura.io/v3/YOUR_PROJECT_ID`)

**Opção C: RPC Público (Não Recomendado para Produção)**
- `https://rpc-mumbai.maticvigil.com`
- `https://matic-mumbai.chainstacklabs.com`

## Deploy dos Smart Contracts

### Passo 1: Configurar Variáveis de Ambiente

```bash
cd /home/ubuntu/bts-blocktrust

# Configurar variáveis de ambiente
export DEPLOYER_PRIVATE_KEY="0xSUA_CHAVE_PRIVADA_AQUI"
export POLYGON_RPC_URL="https://polygon-mumbai.g.alchemy.com/v2/YOUR_API_KEY"
```

### Passo 2: Instalar Dependências

```bash
# Instalar py-solc-x para compilação de contratos
pip3 install py-solc-x web3

# Verificar instalação
python3 -c "from solcx import install_solc; install_solc('0.8.20'); print('✅ Solidity 0.8.20 instalado')"
```

### Passo 3: Executar Deploy

```bash
cd /home/ubuntu/bts-blocktrust
python3 contracts/deploy.py
```

**Saída Esperada:**
```
============================================================
🚀 DEPLOY DE SMART CONTRACTS BLOCKTRUST V1.1
============================================================
✅ Conectado ao Polygon Mumbai: https://polygon-mumbai.g.alchemy.com/v2/...
📍 Deployer Address: 0x6177B7308E60EF9c363205E3AC08f70cc3f04Bd7
💰 Saldo: 0.5 MATIC

📜 FASE 1: Deploy IdentityNFT
------------------------------------------------------------
🔨 Compilando IdentityNFT.sol...
✅ IdentityNFT compilado com sucesso!
🚀 Fazendo deploy de IdentityNFT...
📤 Transação enviada: 0x...
⏳ Aguardando confirmação...
✅ IdentityNFT deployado em: 0xABC123...
🔗 PolygonScan: https://mumbai.polygonscan.com/address/0xABC123...

📜 FASE 2: Deploy ProofRegistry
------------------------------------------------------------
🔨 Compilando ProofRegistry.sol...
✅ ProofRegistry compilado com sucesso!
🚀 Fazendo deploy de ProofRegistry...
📤 Transação enviada: 0x...
⏳ Aguardando confirmação...
✅ ProofRegistry deployado em: 0xDEF456...
🔗 PolygonScan: https://mumbai.polygonscan.com/address/0xDEF456...

📜 FASE 3: Deploy FailSafe
------------------------------------------------------------
🔨 Compilando FailSafe.sol...
✅ FailSafe compilado com sucesso!
🚀 Fazendo deploy de FailSafe...
📤 Transação enviada: 0x...
⏳ Aguardando confirmação...
✅ FailSafe deployado em: 0xGHI789...
🔗 PolygonScan: https://mumbai.polygonscan.com/address/0xGHI789...

🔐 FASE 4: Configurar Roles
------------------------------------------------------------
🔐 Concedendo MINTER_ROLE para 0x6177B7308E60EF9c363205E3AC08f70cc3f04Bd7...
📤 Transação enviada: 0x...
✅ MINTER_ROLE concedida com sucesso!
🔐 Concedendo CANCELER_ROLE para 0xGHI789...
📤 Transação enviada: 0x...
✅ CANCELER_ROLE concedida com sucesso!
🔐 Concedendo SECURITY_ROLE para 0x6177B7308E60EF9c363205E3AC08f70cc3f04Bd7...
📤 Transação enviada: 0x...
✅ SECURITY_ROLE concedida com sucesso!

💾 FASE 5: Salvar Configurações
------------------------------------------------------------
✅ Configurações salvas em .env.contracts
✅ ABIs salvos em contracts/*.abi.json

============================================================
✅ DEPLOY CONCLUÍDO COM SUCESSO!
============================================================

📋 RESUMO DOS CONTRATOS:
  IdentityNFT:    0xABC123...
  ProofRegistry:  0xDEF456...
  FailSafe:       0xGHI789...

🔗 LINKS:
  IdentityNFT:    https://mumbai.polygonscan.com/address/0xABC123...
  ProofRegistry:  https://mumbai.polygonscan.com/address/0xDEF456...
  FailSafe:       https://mumbai.polygonscan.com/address/0xGHI789...

📝 PRÓXIMOS PASSOS:
  1. Copiar endereços para variáveis de ambiente do Render
  2. Atualizar backend/api/utils/nft.py com os novos endereços
  3. Executar testes de integração
============================================================
```

### Passo 4: Atualizar Variáveis de Ambiente no Render

Após o deploy bem-sucedido, você terá um arquivo `.env.contracts` com os endereços dos contratos:

```bash
cat .env.contracts
```

**Copie os endereços e atualize as variáveis de ambiente no Render:**

1. Acesse: https://dashboard.render.com/web/srv-d3v6722li9vc73cj3lsg/env
2. Clique em "Edit"
3. Atualize as seguintes variáveis:
   - `IDENTITY_NFT_ADDRESS` → Endereço do IdentityNFT
   - `PROOF_REGISTRY_ADDRESS` → Endereço do ProofRegistry
   - `FAILSAFE_ADDRESS` → Endereço do FailSafe
   - `DEPLOYER_PRIVATE_KEY` → Chave privada do deployer (mesma usada no deploy)
   - `POLYGON_RPC_URL` → RPC URL da Alchemy/Infura
4. Clique em "Save, rebuild, and deploy"

### Passo 5: Verificar Contratos no PolygonScan

Acesse cada contrato no PolygonScan para verificar:
- Transações de deploy
- Código fonte (opcional: fazer verify)
- Eventos emitidos
- Roles configuradas

## Troubleshooting

### Erro: "Insufficient funds"
**Causa**: Saldo insuficiente de MATIC na carteira.
**Solução**: Obtenha mais MATIC de um faucet.

### Erro: "Nonce too low"
**Causa**: Transação com nonce duplicado.
**Solução**: Aguarde confirmação de transações anteriores ou reinicie o script.

### Erro: "Compilation failed"
**Causa**: Versão do Solidity não instalada.
**Solução**: Execute `python3 -c "from solcx import install_solc; install_solc('0.8.20')"`

### Erro: "RPC connection failed"
**Causa**: RPC URL inválido ou offline.
**Solução**: Verifique o RPC URL e tente outro provider.

## Segurança

⚠️ **IMPORTANTE**:
- **NUNCA** compartilhe sua chave privada
- **NUNCA** faça commit da chave privada no Git
- Use variáveis de ambiente para armazenar chaves
- Para produção, use carteiras de hardware ou serviços de custódia

## Próximos Passos

Após o deploy dos contratos:
1. ✅ Atualizar variáveis de ambiente no Render
2. ✅ Configurar Background Workers (Listener e Monitor)
3. ✅ Executar testes end-to-end
4. ✅ Validar funcionalidades completas

## Suporte

Se encontrar problemas durante o deploy:
- Verifique os logs do script
- Consulte a documentação da Polygon: https://docs.polygon.technology/
- Verifique transações no PolygonScan: https://mumbai.polygonscan.com/
- Entre em contato com o time de desenvolvimento

---

**Versão**: 1.4  
**Data**: Outubro 2025  
**Autor**: Blocktrust Team

