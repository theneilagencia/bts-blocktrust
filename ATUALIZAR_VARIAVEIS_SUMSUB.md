# 🔧 Guia: Atualizar Variáveis Sumsub no Render

## 📋 Variáveis que Precisam Ser Atualizadas

### 1. SUMSUB_APP_TOKEN
**Localização**: Linha "SUMSUB_APP_TOKEN" na lista de variáveis  
**Valor Atual**: (oculto - começa com "prd:..." ou "sbx:...")  
**Novo Valor**: `prd:ePc2R1JUrZwuzplYhv3cwfzJ.UZt9oGTKYbcfA2HNvJevEZBMxymYN754`

### 2. SUMSUB_SECRET_KEY
**Localização**: Linha "SUMSUB_SECRET_KEY" na lista de variáveis  
**Valor Atual**: (oculto)  
**Novo Valor**: `dTgJiI6lFnAXeR2mu4WixaMxrKcn9ggY`

### 3. SUMSUB_LEVEL_NAME
**Localização**: Linha "SUMSUB_LEVEL_NAME" na lista de variáveis  
**Valor Atual**: Provavelmente "basic-kyc-level"  
**Novo Valor**: `basic-kyc`

### 4. MOCK_MODE
**Localização**: Linha "MOCK_MODE" na lista de variáveis  
**Valor Atual**: `false` (já correto)  
**Ação**: ✅ **Manter como está** (não precisa alterar)

---

## 🚀 Passo a Passo

### Passo 1: Acessar Environment
1. Acesse: https://dashboard.render.com/web/srv-d3v6722li9vc73cj3lsg/env
2. Clique no botão **"Edit"** (canto superior direito)

### Passo 2: Atualizar SUMSUB_APP_TOKEN
1. Role a página até encontrar a linha **"SUMSUB_APP_TOKEN"**
2. Clique no campo de **VALUE** (à direita)
3. Apague o valor atual (Ctrl+A, Delete)
4. Cole o novo valor: `prd:ePc2R1JUrZwuzplYhv3cwfzJ.UZt9oGTKYbcfA2HNvJevEZBMxymYN754`

### Passo 3: Atualizar SUMSUB_SECRET_KEY
1. Role a página até encontrar a linha **"SUMSUB_SECRET_KEY"**
2. Clique no campo de **VALUE** (à direita)
3. Apague o valor atual (Ctrl+A, Delete)
4. Cole o novo valor: `dTgJiI6lFnAXeR2mu4WixaMxrKcn9ggY`

### Passo 4: Atualizar SUMSUB_LEVEL_NAME
1. Role a página até encontrar a linha **"SUMSUB_LEVEL_NAME"**
2. Clique no campo de **VALUE** (à direita)
3. Apague o valor atual (Ctrl+A, Delete)
4. Cole o novo valor: `basic-kyc`

### Passo 5: Verificar MOCK_MODE
1. Role a página até encontrar a linha **"MOCK_MODE"**
2. Verifique se o valor é **"false"**
3. ✅ Se for "false", não precisa alterar
4. ❌ Se for "true", altere para "false"

### Passo 6: Salvar e Fazer Deploy
1. Role até o final da página
2. Clique no botão **"Save, rebuild, and deploy"**
3. Aguarde o deploy completar (2-3 minutos)

---

## ✅ Verificação Pós-Deploy

Após o deploy completar, execute este teste:

```bash
# 1. Criar conta de teste
curl -X POST https://bts-blocktrust.onrender.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test_sumsub_'$(date +%s)'@example.com",
    "password": "TestPass123!",
    "coercion_password": "EmergencyPass456!"
  }'

# Copie o token retornado e use no próximo comando

# 2. Iniciar KYC (substitua <TOKEN> pelo token recebido)
curl -X POST https://bts-blocktrust.onrender.com/api/kyc/init \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json"
```

### Resultado Esperado ✅

```json
{
  "status": "success",
  "accessToken": "act-...",  ← Token REAL da Sumsub
  "applicantId": "67...",     ← ID REAL (não "mock_applicant_...")
  "expiresAt": "2025-...",
  "mock_mode": false          ← DEVE SER FALSE
}
```

### Resultado INCORRETO ❌

```json
{
  "status": "success",
  "accessToken": "mock_access_token_for_testing",  ← MOCK!
  "applicantId": "mock_applicant_123",             ← MOCK!
  "mock_mode": true,                               ← MOCK ATIVO!
  "message": "Mock: ..."
}
```

Se o resultado for INCORRETO:
1. Verifique se as variáveis foram salvas corretamente
2. Verifique os logs do Render: https://dashboard.render.com/web/srv-d3v6722li9vc73cj3lsg/logs
3. Procure por erros como "HMAC_SIGNATURE_ERROR" ou "API_ERROR"

---

## 🔍 Troubleshooting

### Erro: "HMAC_SIGNATURE_ERROR"
**Causa**: SUMSUB_SECRET_KEY incorreta  
**Solução**: Verifique se a Secret Key foi copiada corretamente (sem espaços extras)

### Erro: "Unauthorized" ou "401"
**Causa**: SUMSUB_APP_TOKEN incorreto ou expirado  
**Solução**: Verifique se o App Token foi copiado corretamente e se está no formato `prd:...`

### Erro: "levelName not found"
**Causa**: SUMSUB_LEVEL_NAME incorreto  
**Solução**: Verifique no painel Sumsub qual é o nome correto do level (deve ser "basic-kyc")

### Ainda retorna "mock_mode: true"
**Causa**: Código ainda tem fallbacks mock  
**Solução**: Verifique se o último commit (`143b45f`) foi deployado corretamente

---

## 📊 Status das Alterações

### Backend ✅
- [x] Remover fallbacks mock de `sumsub.py`
- [x] Remover fallbacks mock de `kyc_routes.py`
- [x] Commit `143b45f` enviado para GitHub
- [x] Auto-deploy ativado no Render

### Variáveis de Ambiente ⏳
- [ ] SUMSUB_APP_TOKEN atualizado
- [ ] SUMSUB_SECRET_KEY atualizado
- [ ] SUMSUB_LEVEL_NAME atualizado
- [x] MOCK_MODE = false (já configurado)

### Testes ⏳
- [ ] Criar conta de teste
- [ ] Iniciar KYC
- [ ] Verificar que `mock_mode: false`
- [ ] Verificar que `applicantId` é real

---

## 🎯 Próximos Passos

Após atualizar as variáveis e validar que está funcionando:

1. ✅ **Fase 2 CONCLUÍDA**: Variáveis de ambiente configuradas
2. 🚀 **Fase 3**: Ajustar listener de eventos blockchain
3. 🎨 **Fase 4**: Corrigir frontend React com tratamento de erros
4. 🧪 **Fase 5**: Criar testes automatizados
5. 📊 **Fase 6**: Validação final e relatório

---

**Criado por**: Manus AI  
**Data**: 29 de Outubro de 2025  
**Versão**: 1.0

