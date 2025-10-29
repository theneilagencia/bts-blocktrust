# Preparação do Ambiente de Produção - Blocktrust v1.4

**Data**: 28 de outubro de 2025, 20:00 GMT-3  
**Versão**: 1.4  
**Último Commit**: `47112e2` - Correção massiva de imports

---

## ✅ Status Atual

### **Código**
- ✅ Todos os imports corrigidos e validados localmente
- ✅ Dependências atualizadas no `requirements.txt`
- ✅ Compatibilidade com web3.py >= 6.0
- ✅ Todos os fluxos implementados

### **Deploy**
- ⏳ Commit `47112e2` enviado para GitHub
- ⏳ Render detectará automaticamente e iniciará deploy
- ⏳ Estimativa: 3-5 minutos para conclusão

---

## 🔧 Correções Aplicadas

### **1. Imports de Autenticação**
**Problema**: `ModuleNotFoundError: No module named 'api.utils.auth'`  
**Solução**: Alterado `api.utils.auth` → `api.auth` em 4 arquivos

### **2. Imports de Banco de Dados**
**Problema**: `ModuleNotFoundError: No module named 'api.utils.database'`  
**Solução**: Alterado `api.utils.database` → `api.utils.db` em 5 arquivos

### **3. Middleware do Web3**
**Problema**: `ImportError: cannot import name 'geth_poa_middleware'`  
**Solução**: Removido `geth_poa_middleware` (não é mais necessário no web3.py >= 6.0)

---

## 📋 Checklist de Preparação

### **Fase 1: Aguardar Deploy** ⏳
- [ ] Deploy do commit `47112e2` concluído com sucesso
- [ ] Serviço online em `https://bts-blocktrust.onrender.com`
- [ ] Health check retornando 200 OK

### **Fase 2: Aplicar Migrations** 🔄
```bash
# Conectar ao banco de dados PostgreSQL
psql $DATABASE_URL

# Aplicar migrations na ordem
\i backend/migrations/001_initial_schema.sql
\i backend/migrations/002_add_wallet_fields.sql
\i backend/migrations/003_add_nft_tables.sql
\i backend/migrations/004_add_pgp_tables.sql
\i backend/migrations/005_failsafe_password.sql

# Verificar tabelas criadas
\dt

# Sair
\q
```

### **Fase 3: Verificar Variáveis de Ambiente** 🔐
Garantir que as seguintes variáveis estão configuradas no Render:

**Obrigatórias**:
- `DATABASE_URL` - URL do PostgreSQL
- `JWT_SECRET` - Secret para tokens JWT
- `SUMSUB_APP_TOKEN` - Token da API Sumsub
- `SUMSUB_SECRET_KEY` - Secret Key da API Sumsub

**Blockchain** (opcional para testes):
- `POLYGON_RPC_URL` - URL do RPC do Polygon Mumbai
- `DEPLOYER_PRIVATE_KEY` - Chave privada para deploy de contratos
- `IDENTITY_NFT_CONTRACT_ADDRESS` - Endereço do contrato IdentityNFT
- `PROOF_REGISTRY_CONTRACT_ADDRESS` - Endereço do contrato ProofRegistry
- `FAILSAFE_CONTRACT_ADDRESS` - Endereço do contrato FailSafe

**Monitoramento** (opcional):
- `SLACK_WEBHOOK_URL` - Webhook do Slack para alertas
- `TELEGRAM_BOT_TOKEN` - Token do bot do Telegram
- `TELEGRAM_CHAT_ID` - ID do chat do Telegram

### **Fase 4: Iniciar Workers** 🚀
Configurar Background Workers no Render:

**Worker 1: Listener de Eventos**
- Comando: `python3 backend/listener.py`
- Instâncias: 1
- Tipo: Background Worker

**Worker 2: Monitor de Saúde**
- Comando: `python3 -m backend.monitor.runner`
- Instâncias: 1
- Tipo: Background Worker

### **Fase 5: Executar Testes de Validação** 🧪
```bash
# Executar script de validação completa
python3 validate_all_flows.py

# Executar testes Pytest
cd backend
pytest tests/ -v
```

### **Fase 6: Validar Fluxos Manualmente** 👤
1. **Cadastro**:
   - Criar usuário com senha normal e senha de coação
   - Verificar que ambas as senhas foram salvas

2. **KYC → NFT**:
   - Iniciar processo de KYC
   - Verificar que NFT é mintado automaticamente após aprovação

3. **Assinatura Normal**:
   - Assinar documento com senha normal
   - Verificar que assinatura é registrada na blockchain

4. **Assinatura Failsafe**:
   - Assinar documento com senha de coação
   - Verificar que NFT é cancelado automaticamente
   - Verificar que evento é registrado em `failsafe_events`

---

## 🔍 Monitoramento Pós-Deploy

### **Logs a Monitorar**
```bash
# Logs do serviço principal
# Acessar via Render Dashboard → Logs

# Verificar:
- ✅ Servidor iniciado sem erros
- ✅ Conexão com banco de dados OK
- ✅ Rotas registradas corretamente
- ✅ Sem erros de import
```

### **Endpoints a Testar**
```bash
# Health check
curl https://bts-blocktrust.onrender.com/api/health

# Failsafe status (requer autenticação)
curl -H "Authorization: Bearer $TOKEN" \
  https://bts-blocktrust.onrender.com/api/failsafe/status

# Explorer events
curl -H "Authorization: Bearer $TOKEN" \
  https://bts-blocktrust.onrender.com/api/explorer/events
```

### **Métricas a Acompanhar**
- **Latência**: < 800ms (SLO)
- **Uptime**: >= 99.5% (SLO)
- **Taxa de Erro**: < 1%
- **Listener Lag**: < 180s

---

## 🚨 Plano de Rollback

Se o deploy falhar ou houver problemas críticos:

### **Opção 1: Rollback via Render**
1. Acessar Render Dashboard
2. Ir para Events
3. Clicar em "Rollback" no último deploy bem-sucedido

### **Opção 2: Rollback via Git**
```bash
# Reverter para último commit estável
git revert 47112e2
git push

# Ou fazer rollback completo
git reset --hard <commit_anterior_estavel>
git push --force
```

### **Último Deploy Estável Conhecido**
- **Commit**: (a ser determinado após primeiro deploy bem-sucedido)
- **Data**: (a ser determinado)

---

## 📊 Critérios de Sucesso

O deploy será considerado bem-sucedido quando:

1. ✅ Serviço iniciado sem erros
2. ✅ Health check retornando 200 OK
3. ✅ Todos os endpoints respondendo
4. ✅ Migrations aplicadas com sucesso
5. ✅ Cadastro de usuário funcionando
6. ✅ Fluxo KYC → NFT funcionando
7. ✅ Assinatura normal funcionando
8. ✅ **Assinatura failsafe funcionando**
9. ✅ Listener de eventos operacional
10. ✅ Monitor de saúde operacional

---

## 📝 Próximos Passos

1. ⏳ **Aguardar deploy do commit `47112e2`** (3-5 min)
2. ✅ **Verificar logs** para confirmar sucesso
3. ✅ **Aplicar migrations** no banco de dados
4. ✅ **Executar testes de validação**
5. ✅ **Validar fluxos manualmente**
6. ✅ **Iniciar workers** (listener e monitor)
7. ✅ **Monitorar métricas** por 24h
8. ✅ **Gerar relatório final** de validação

---

## 🎯 Objetivo Final

**Sistema 100% funcional em produção com todos os fluxos validados, incluindo a jornada failsafe completa.**

---

**Preparado por**: Manus AI Agent  
**Última atualização**: 28 de outubro de 2025, 20:00 GMT-3

