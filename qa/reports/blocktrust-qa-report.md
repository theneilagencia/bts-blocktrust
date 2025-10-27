# Relatório de QA - BTS Blocktrust

**Data:** 2025-10-27T17:04:21.901162

## Resumo Executivo

- **Total de Testes:** 26
- **✅ Passaram:** 20
- **❌ Falharam:** 3
- **⚠️ Avisos:** 3
- **Taxa de Sucesso:** 76.9%

## Latência Média por Módulo

| Módulo | Latência Média | Status |
|--------|----------------|--------|
| Backend | 260.98ms | ✅ OK |
| Auth | 524.32ms | ⚠️ Alto |
| KYC | 381.81ms | ✅ OK |
| Security | 240.57ms | ✅ OK |
| Blockchain | 6274.81ms | ⚠️ Alto |
| Failsafe | 303.57ms | ✅ OK |
| Frontend | 193.03ms | ✅ OK |

## Detalhes dos Testes

### Backend - Health Check

- **Status:** ✅ PASS
- **Latência:** 260.98ms
- **Detalhes:** Status 200

### Auth - Registro de Usuário

- **Status:** ✅ PASS
- **Latência:** 680.84ms
- **Detalhes:** Status 201

### Auth - Login de Usuário

- **Status:** ✅ PASS
- **Latência:** 661.12ms
- **Detalhes:** Status 200

### Auth - Login Inválido (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 849.79ms
- **Detalhes:** Status 401

### Auth - Acesso sem Token (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 210.91ms
- **Detalhes:** Status 401

### Auth - Token Inválido (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 218.93ms
- **Detalhes:** Status 401

### KYC - Inicializar KYC

- **Status:** ✅ PASS
- **Latência:** 451.21ms
- **Detalhes:** Status 200

### KYC - Consultar Status KYC

- **Status:** ❌ FAIL
- **Latência:** 449.83ms
- **Detalhes:** Expected [200], got 500

### KYC - Consultar Liveness Status

- **Status:** ❌ FAIL
- **Latência:** 433.28ms
- **Detalhes:** Expected [200], got 500

### KYC - Webhook Sumsub (simulado)

- **Status:** ❌ FAIL
- **Latência:** 192.89ms
- **Detalhes:** Expected [200], got 401

### Security - Webhook sem Assinatura (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 188.58ms
- **Detalhes:** Status 401

### Security - Webhook com Assinatura Inválida (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 188.97ms
- **Detalhes:** Status 401

### Blockchain - Verificar Documento

- **Status:** ✅ PASS
- **Latência:** 6348.66ms
- **Detalhes:** Status 200

### Blockchain - Registrar Assinatura

- **Status:** ✅ PASS
- **Latência:** 6250.81ms
- **Detalhes:** Status 200

### Blockchain - Mint Identity

- **Status:** ✅ PASS
- **Latência:** 6224.95ms
- **Detalhes:** Status 200

### Failsafe - Ativar Botão de Pânico

- **Status:** ✅ PASS
- **Latência:** 347.05ms
- **Detalhes:** Status 200

### Failsafe - Pânico sem Autenticação (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 246.14ms
- **Detalhes:** Status 401

### Failsafe - Pânico com Dados Parciais

- **Status:** ✅ PASS
- **Latência:** 317.53ms
- **Detalhes:** Status 200

### Security - SQL Injection (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 392.87ms
- **Detalhes:** Status 400

### Security - XSS no Email (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 279.09ms
- **Detalhes:** Status 400

### Security - Registro sem Senha (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 210.15ms
- **Detalhes:** Status 400

### Security - Login sem Email (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 183.74ms
- **Detalhes:** Status 400

### Frontend - Página Inicial

- **Status:** ✅ PASS
- **Latência:** 184.37ms
- **Detalhes:** HTML carregado

### Frontend - Asset /assets/index.css

- **Status:** ⚠️ WARN
- **Latência:** 202.44ms
- **Detalhes:** Status 404

### Frontend - Asset /assets/index.js

- **Status:** ⚠️ WARN
- **Latência:** 178.08ms
- **Detalhes:** Status 404

### Frontend - Logo

- **Status:** ⚠️ WARN
- **Latência:** 207.24ms
- **Detalhes:** Status 404

