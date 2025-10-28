# Blocktrust v1.4 - Guia de Deploy em Produção

**Data**: 28 de outubro de 2025  
**Versão**: 1.4 (Production Ready)  
**Status**: ✅ **Pronto para Deploy**

---

## 📋 Pré-requisitos

### Variáveis de Ambiente Obrigatórias

```bash
# Banco de Dados
DATABASE_URL=postgresql+psycopg2://user:password@host:port/database

# Blockchain
POLYGON_RPC_URL=https://polygon-mumbai.infura.io/v3/YOUR_KEY
DEPLOYER_PRIVATE_KEY=0x...

# Sumsub KYC
SUMSUB_APP_TOKEN=your_app_token
SUMSUB_SECRET_KEY=your_secret_key
SUMSUB_LEVEL_NAME=basic-kyc-level

# JWT
JWT_SECRET=your_jwt_secret_key

# Monitoramento (Opcional)
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# S3 Backup (Opcional)
S3_BUCKET=blocktrust-backups
S3_ACCESS_KEY=your_access_key
S3_SECRET_KEY=your_secret_key
```

---

## 🚀 Passo a Passo de Deploy

### 1. Preparação do Ambiente

```bash
# Clone o repositório
git clone https://github.com/theneilagencia/bts-blocktrust.git
cd bts-blocktrust

# Checkout da versão v1.4
git checkout master

# Build completo
bash build.sh
```

### 2. Deploy dos Smart Contracts

```bash
# Instalar dependências do Hardhat
npm install

# Compilar contratos
npx hardhat compile

# Deploy no Polygon Mumbai
npx hardhat run scripts/deploy.js --network polygonMumbai

# Salvar endereços em backend/config/contracts.json
```

**Contratos a serem deployados**:
- `IdentityNFT.sol` - NFT SoulBound de identidade
- `ProofRegistry.sol` - Registro de provas de documentos
- `FailSafe.sol` - Sistema de emergência

### 3. Configurar Roles nos Contratos

```bash
# Executar script de configuração de roles
npx hardhat run scripts/setup_roles.js --network polygonMumbai
```

**Roles necessárias**:
- `MINTER_ROLE` - Permissão para mintar NFTs
- `CANCELER_ROLE` - Permissão para cancelar NFTs
- `SECURITY_ROLE` - Permissão para acionar FailSafe

### 4. Aplicar Migrations no Banco de Dados

```bash
# Conectar ao PostgreSQL
psql $DATABASE_URL

# Aplicar migrations
\i backend/migrations/001_initial_schema.sql
\i backend/migrations/002_wallet_nft.sql
\i backend/migrations/003_signature_failsafe.sql
\i backend/migrations/004_pgp_dual_signature.sql
```

### 5. Iniciar Serviços

#### Backend Flask

```bash
cd backend
python3 app.py
```

**Porta**: 10000  
**Health Check**: `http://localhost:10000/api/health`

#### Listener Blockchain

```bash
cd backend
python3 listener.py
```

**Função**: Monitora eventos da blockchain em tempo real

#### Monitor

```bash
cd backend
python3 -m monitor.runner
```

**Função**: Health checks, testes sintéticos e alertas

### 6. Validar Deploy

```bash
# Executar testes de smoke
curl http://localhost:10000/api/health

# Executar testes automatizados
cd backend
pytest tests/ -v
```

---

## 🔐 Segurança

### Rate Limiting

- **Importação PGP**: 5 por hora
- **Assinatura Dupla**: 20 por hora
- **Requisições Gerais**: 200 por dia, 50 por hora

### Auditoria

Todas as ações sensíveis são registradas com:
- IP do usuário
- User-Agent
- Timestamp
- Resultado da operação

### Chaves Privadas

- **NUNCA** armazenar chaves privadas PGP
- **NUNCA** expor `DEPLOYER_PRIVATE_KEY` em logs
- **SEMPRE** usar variáveis de ambiente

---

## 📊 Monitoramento

### Métricas SLO

| Métrica | Target | Descrição |
|---------|--------|-----------|
| API Latency (P99) | < 800ms | Latência do endpoint `/api/health` |
| Uptime | ≥ 99.5% | Disponibilidade da API |
| Listener Lag | < 180s | Atraso do listener blockchain |

### Alertas

O sistema envia alertas automáticos quando:
- API está indisponível
- Listener está atrasado (> 3 minutos)
- Testes sintéticos falham
- SLO é violado

---

## 🧪 Testes de Validação

### Smoke Tests

```bash
# 1. Health Check
curl http://localhost:10000/api/health
# Esperado: 200 OK

# 2. Criar usuário
curl -X POST http://localhost:10000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!","name":"Test User"}'

# 3. Login
curl -X POST http://localhost:10000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'

# 4. Importar chave PGP
curl -X POST http://localhost:10000/api/pgp/import \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"armored_pubkey":"-----BEGIN PGP PUBLIC KEY BLOCK-----..."}'

# 5. Criar assinatura dupla
curl -X POST http://localhost:10000/api/dual/sign \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"doc_hash":"0x...","pgp_signature":"...","pgp_fingerprint":"...","nft_id":1}'
```

### QA Automatizados

```bash
cd backend
pytest tests/test_dual_signature.py -v
```

**Esperado**: 100% PASS

---

## 📂 Estrutura de Arquivos

```
bts-blocktrust/
├── contracts/              # Smart Contracts Solidity
│   ├── IdentityNFT.sol
│   ├── ProofRegistry.sol
│   └── FailSafe.sol
├── scripts/                # Scripts de deploy
│   ├── deploy.js
│   └── setup_roles.js
├── backend/                # Backend Flask
│   ├── app.py
│   ├── listener.py
│   ├── api/
│   │   ├── routes/         # Rotas da API
│   │   ├── utils/          # Utilitários
│   │   └── middleware/     # Middleware de segurança
│   ├── monitor/            # Sistema de monitoramento
│   ├── migrations/         # Migrations SQL
│   └── tests/              # Testes automatizados
├── frontend/               # Frontend React
│   └── src/
│       ├── components/
│       └── app/
└── docs/                   # Documentação
    ├── BLOCKTRUST_V1.4_DUAL_SIGNATURE.md
    ├── MONITORING_GUIDE.md
    └── PRODUCTION_DEPLOYMENT_GUIDE.md
```

---

## 🆘 Troubleshooting

### Problema: API não inicia

**Solução**:
```bash
# Verificar variáveis de ambiente
env | grep -E "DATABASE_URL|JWT_SECRET"

# Verificar logs
tail -f backend/logs/app.log
```

### Problema: Listener não captura eventos

**Solução**:
```bash
# Verificar RPC URL
curl $POLYGON_RPC_URL

# Verificar endereços dos contratos
cat backend/config/contracts.json

# Reiniciar listener
pkill -f listener.py
python3 backend/listener.py
```

### Problema: Testes falhando

**Solução**:
```bash
# Limpar banco de dados de teste
psql $DATABASE_URL -c "DROP DATABASE IF EXISTS blocktrust_test;"
psql $DATABASE_URL -c "CREATE DATABASE blocktrust_test;"

# Reexecutar migrations
\i backend/migrations/*.sql

# Executar testes novamente
pytest tests/ -v
```

---

## 📚 Referências

- [Documentação v1.4](./BLOCKTRUST_V1.4_DUAL_SIGNATURE.md)
- [Guia de Monitoramento](./MONITORING_GUIDE.md)
- [Polygon Mumbai Explorer](https://mumbai.polygonscan.com/)
- [Sumsub API Documentation](https://developers.sumsub.com/)

---

## ✅ Checklist de Deploy

- [ ] Variáveis de ambiente configuradas
- [ ] Contratos deployados no Polygon Mumbai
- [ ] Roles configuradas nos contratos
- [ ] Migrations aplicadas no banco de dados
- [ ] Backend Flask iniciado
- [ ] Listener blockchain iniciado
- [ ] Monitor iniciado
- [ ] Smoke tests executados com sucesso
- [ ] QA automatizados 100% PASS
- [ ] Alertas configurados (Slack/Telegram)
- [ ] Backups configurados (S3)

---

**Status**: ✅ **Sistema Pronto para Produção**

*Guia gerado automaticamente por Manus AI Agent*

