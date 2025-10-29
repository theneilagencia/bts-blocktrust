# Status das Variáveis de Ambiente - Blocktrust v1.4

## Data: 2025-10-28 21:02

## Problema Detectado
- ❌ **SUMSUB_SECRET_KEY está duplicada**
- Existe uma variável SUMSUB_SECRET_KEY original (index 41)
- Foi adicionada uma segunda SUMSUB_SECRET_KEY (index 85)
- Render não permite chaves duplicadas

## Variáveis Já Existentes (Originais)
1. ALERT_EMAILS
2. DATABASE_URL
3. FROM_EMAIL
4. JWT_SECRET
5. NODE_VERSION
6. PYTHON_VERSION
7. SENDGRID_API_KEY
8. SUMSUB_APP_TOKEN
9. SUMSUB_LEVEL_NAME
10. SUMSUB_SECRET_KEY ← **JÁ EXISTE**
11. TOOLBLOX_MINT_IDENTITY_URL
12. TOOLBLOX_NETWORK
13. TOOLBLOX_REGISTER_SIGNATURE_URL
14. TOOLBLOX_VERIFY_URL

## Variáveis Adicionadas com Sucesso
1. ✅ NETWORK = polygonMumbai
2. ✅ POLYGON_RPC_URL = https://polygon-mumbai.g.alchemy.com/v2/demo
3. ✅ DEPLOYER_PRIVATE_KEY = 0x0000... (placeholder)
4. ✅ IDENTITY_NFT_ADDRESS = 0x0000... (placeholder)
5. ✅ PROOF_REGISTRY_ADDRESS = 0x0000... (placeholder)
6. ✅ FAILSAFE_ADDRESS = 0x0000... (placeholder)
7. ✅ MOCK_MODE = false
8. ✅ SLO_LATENCY_MS = 800
9. ✅ SLO_UPTIME_TARGET = 99.5

## Variável Duplicada (Precisa Remover)
- ❌ SUMSUB_SECRET_KEY = PLACEHOLDER_SECRET_KEY (segunda ocorrência)

## Ação Necessária
1. Remover a segunda ocorrência de SUMSUB_SECRET_KEY (index 85)
2. Salvar e fazer deploy
3. Aplicar migrations no banco de dados
4. Configurar Background Workers

