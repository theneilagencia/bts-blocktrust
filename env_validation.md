# Validação de Variáveis de Ambiente - Render

## Variáveis Identificadas

Baseado na visualização do Render, as seguintes variáveis estão configuradas:

1. ✅ `ALERT_EMAILS` - Configurado
2. ✅ `DATABASE_URL` - Configurado
3. ✅ `FROM_EMAIL` - Configurado
4. ✅ `JWT_SECRET` - Configurado
5. ✅ `NODE_VERSION` - Configurado
6. ✅ `PYTHON_VERSION` - Configurado
7. ✅ `SENDGRID_API_KEY` - Configurado
8. ✅ `SUMSUB_APP_TOKEN` - Configurado
9. ✅ `SUMSUB_LEVEL_NAME` - Configurado

## Variáveis Faltantes (Conforme Especificação)

Baseado na especificação v1.2, as seguintes variáveis estão FALTANDO:

1. ❌ `NETWORK` - Deve ser `polygonMumbai`
2. ❌ `RPC_URL` ou `POLYGON_RPC_URL` - URL do RPC do Polygon Mumbai
3. ❌ `PRIVATE_KEY_DEPLOYER` ou `DEPLOYER_PRIVATE_KEY` - Chave privada para deploy de contratos
4. ❌ `IDENTITY_NFT_ADDRESS` - Endereço do contrato IdentityNFT
5. ❌ `PROOF_REGISTRY_ADDRESS` - Endereço do contrato ProofRegistry
6. ❌ `FAILSAFE_ADDRESS` - Endereço do contrato FailSafe
7. ❌ `SUMSUB_SECRET_KEY` - Secret key do Sumsub
8. ❌ `MOCK_MODE` - Deve ser `false` para produção
9. ❌ `SLO_LATENCY_MS` - Deve ser `800`
10. ❌ `SLO_UPTIME_TARGET` - Deve ser `99.5`

## Ação Necessária

Preciso adicionar as variáveis faltantes no Render para que o sistema funcione corretamente.

