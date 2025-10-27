# Relatório de QA - BTS Blocktrust

**Data:** 2025-10-27T16:18:08.137526

## Resumo Executivo

- **Total de Testes:** 26
- **✅ Passaram:** 15
- **❌ Falharam:** 8
- **⚠️ Avisos:** 3
- **Taxa de Sucesso:** 57.7%

## Latência Média por Módulo

| Módulo | Latência Média | Status |
|--------|----------------|--------|
| Backend | 241.81ms | ✅ OK |
| Auth | 510.11ms | ⚠️ Alto |
| KYC | 267.43ms | ✅ OK |
| Security | 278.98ms | ✅ OK |
| Blockchain | 4227.94ms | ⚠️ Alto |
| Failsafe | 291.45ms | ✅ OK |
| Frontend | 210.65ms | ✅ OK |

## Detalhes dos Testes

### Backend - Health Check

- **Status:** ✅ PASS
- **Latência:** 241.81ms
- **Detalhes:** Status 200

### Auth - Registro de Usuário

- **Status:** ✅ PASS
- **Latência:** 660.83ms
- **Detalhes:** Status 201

### Auth - Login de Usuário

- **Status:** ✅ PASS
- **Latência:** 822.82ms
- **Detalhes:** Status 200

### Auth - Login Inválido (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 616.87ms
- **Detalhes:** Status 401

### Auth - Acesso sem Token (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 211.55ms
- **Detalhes:** Status 401

### Auth - Token Inválido (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 238.46ms
- **Detalhes:** Status 401

### KYC - Inicializar KYC

- **Status:** ❌ FAIL
- **Latência:** 186.77ms
- **Detalhes:** Expected 200, got 500

### KYC - Consultar Status KYC

- **Status:** ❌ FAIL
- **Latência:** 201.39ms
- **Detalhes:** Expected 200, got 500

### KYC - Consultar Liveness Status

- **Status:** ❌ FAIL
- **Latência:** 489.65ms
- **Detalhes:** Expected 200, got 500

### KYC - Webhook Sumsub (simulado)

- **Status:** ❌ FAIL
- **Latência:** 191.93ms
- **Detalhes:** Expected 200, got 401

### Security - Webhook sem Assinatura (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 180.39ms
- **Detalhes:** Status 401

### Security - Webhook com Assinatura Inválida (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 230.37ms
- **Detalhes:** Status 401

### Blockchain - Verificar Documento

- **Status:** ❌ FAIL
- **Latência:** 6228.98ms
- **Detalhes:** Expected 200, got 500

### Blockchain - Registrar Assinatura

- **Status:** ❌ FAIL
- **Latência:** 6216.09ms
- **Detalhes:** Expected 200, got 500

### Blockchain - Mint Identity

- **Status:** ❌ FAIL
- **Latência:** 238.77ms
- **Detalhes:** Expected 200, got 400

### Failsafe - Ativar Botão de Pânico

- **Status:** ✅ PASS
- **Latência:** 349.81ms
- **Detalhes:** Status 200

### Failsafe - Pânico sem Autenticação (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 208.55ms
- **Detalhes:** Status 401

### Failsafe - Pânico com Dados Parciais

- **Status:** ✅ PASS
- **Latência:** 316.0ms
- **Detalhes:** Status 200

### Security - SQL Injection (deve falhar)

- **Status:** ❌ FAIL
- **Latência:** 500.99ms
- **Detalhes:** Expected 401, got 400

### Security - XSS no Email (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 228.26ms
- **Detalhes:** Status 400

### Security - Registro sem Senha (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 353.74ms
- **Detalhes:** Status 400

### Security - Login sem Email (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 180.16ms
- **Detalhes:** Status 400

### Frontend - Página Inicial

- **Status:** ✅ PASS
- **Latência:** 198.58ms
- **Detalhes:** HTML carregado

### Frontend - Asset /assets/index.css

- **Status:** ⚠️ WARN
- **Latência:** 186.45ms
- **Detalhes:** Status 404

### Frontend - Asset /assets/index.js

- **Status:** ⚠️ WARN
- **Latência:** 243.01ms
- **Detalhes:** Status 404

### Frontend - Logo

- **Status:** ⚠️ WARN
- **Latência:** 214.56ms
- **Detalhes:** Status 404

