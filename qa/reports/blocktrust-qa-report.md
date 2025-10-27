# Relatório de QA - BTS Blocktrust

**Data:** 2025-10-27T10:57:24.306404

## Resumo Executivo

- **Total de Testes:** 26
- **✅ Passaram:** 15
- **❌ Falharam:** 8
- **⚠️ Avisos:** 3
- **Taxa de Sucesso:** 57.7%

## Latência Média por Módulo

| Módulo | Latência Média | Status |
|--------|----------------|--------|
| Backend | 199.58ms | ✅ OK |
| Auth | 467.18ms | ✅ OK |
| KYC | 207.94ms | ✅ OK |
| Security | 228.18ms | ✅ OK |
| Blockchain | 204.31ms | ✅ OK |
| Failsafe | 266.61ms | ✅ OK |
| Frontend | 196.25ms | ✅ OK |

## Detalhes dos Testes

### Backend - Health Check

- **Status:** ✅ PASS
- **Latência:** 199.58ms
- **Detalhes:** Status 200

### Auth - Registro de Usuário

- **Status:** ✅ PASS
- **Latência:** 638.0ms
- **Detalhes:** Status 201

### Auth - Login de Usuário

- **Status:** ✅ PASS
- **Latência:** 656.6ms
- **Detalhes:** Status 200

### Auth - Login Inválido (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 637.83ms
- **Detalhes:** Status 401

### Auth - Acesso sem Token (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 221.44ms
- **Detalhes:** Status 401

### Auth - Token Inválido (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 182.05ms
- **Detalhes:** Status 401

### KYC - Inicializar KYC

- **Status:** ❌ FAIL
- **Latência:** 216.4ms
- **Detalhes:** Expected 200, got 500

### KYC - Consultar Status KYC

- **Status:** ❌ FAIL
- **Latência:** 210.54ms
- **Detalhes:** Expected 200, got 500

### KYC - Consultar Liveness Status

- **Status:** ❌ FAIL
- **Latência:** 194.65ms
- **Detalhes:** Expected 200, got 500

### KYC - Webhook Sumsub (simulado)

- **Status:** ❌ FAIL
- **Latência:** 210.18ms
- **Detalhes:** Expected 200, got 401

### Security - Webhook sem Assinatura (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 151.03ms
- **Detalhes:** Status 401

### Security - Webhook com Assinatura Inválida (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 171.01ms
- **Detalhes:** Status 401

### Blockchain - Verificar Documento

- **Status:** ❌ FAIL
- **Latência:** 175.01ms
- **Detalhes:** Expected 200, got 400

### Blockchain - Registrar Assinatura

- **Status:** ❌ FAIL
- **Latência:** 224.5ms
- **Detalhes:** Expected 200, got 400

### Blockchain - Mint Identity

- **Status:** ❌ FAIL
- **Latência:** 213.41ms
- **Detalhes:** Expected 200, got 400

### Failsafe - Ativar Botão de Pânico

- **Status:** ✅ PASS
- **Latência:** 302.66ms
- **Detalhes:** Status 200

### Failsafe - Pânico sem Autenticação (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 199.01ms
- **Detalhes:** Status 401

### Failsafe - Pânico com Dados Parciais

- **Status:** ✅ PASS
- **Latência:** 298.16ms
- **Detalhes:** Status 200

### Security - SQL Injection (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 404.68ms
- **Detalhes:** Status 401

### Security - XSS no Email (deve falhar)

- **Status:** ❌ FAIL
- **Latência:** 197.77ms
- **Detalhes:** Expected 400, got 409

### Security - Registro sem Senha (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 214.02ms
- **Detalhes:** Status 400

### Security - Login sem Email (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 230.59ms
- **Detalhes:** Status 400

### Frontend - Página Inicial

- **Status:** ✅ PASS
- **Latência:** 187.67ms
- **Detalhes:** HTML carregado

### Frontend - Asset /assets/index.css

- **Status:** ⚠️ WARN
- **Latência:** 200.38ms
- **Detalhes:** Status 404

### Frontend - Asset /assets/index.js

- **Status:** ⚠️ WARN
- **Latência:** 214.99ms
- **Detalhes:** Status 404

### Frontend - Logo

- **Status:** ⚠️ WARN
- **Latência:** 181.97ms
- **Detalhes:** Status 404

