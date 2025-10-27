# Relatório de QA - BTS Blocktrust

**Data:** 2025-10-27T16:24:54.397276

## Resumo Executivo

- **Total de Testes:** 26
- **✅ Passaram:** 17
- **❌ Falharam:** 6
- **⚠️ Avisos:** 3
- **Taxa de Sucesso:** 65.4%

## Latência Média por Módulo

| Módulo | Latência Média | Status |
|--------|----------------|--------|
| Backend | 234.53ms | ✅ OK |
| Auth | 474.71ms | ✅ OK |
| KYC | 358.33ms | ✅ OK |
| Security | 243.88ms | ✅ OK |
| Blockchain | 4252.96ms | ⚠️ Alto |
| Failsafe | 356.35ms | ✅ OK |
| Frontend | 197.48ms | ✅ OK |

## Detalhes dos Testes

### Backend - Health Check

- **Status:** ✅ PASS
- **Latência:** 234.53ms
- **Detalhes:** Status 200

### Auth - Registro de Usuário

- **Status:** ✅ PASS
- **Latência:** 691.37ms
- **Detalhes:** Status 201

### Auth - Login de Usuário

- **Status:** ✅ PASS
- **Latência:** 647.4ms
- **Detalhes:** Status 200

### Auth - Login Inválido (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 661.69ms
- **Detalhes:** Status 401

### Auth - Acesso sem Token (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 174.93ms
- **Detalhes:** Status 401

### Auth - Token Inválido (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 198.18ms
- **Detalhes:** Status 401

### KYC - Inicializar KYC

- **Status:** ❌ FAIL
- **Latência:** 505.98ms
- **Detalhes:** Expected 200, got 500

### KYC - Consultar Status KYC

- **Status:** ✅ PASS
- **Latência:** 389.49ms
- **Detalhes:** Status 200

### KYC - Consultar Liveness Status

- **Status:** ✅ PASS
- **Latência:** 198.03ms
- **Detalhes:** Status 200

### KYC - Webhook Sumsub (simulado)

- **Status:** ❌ FAIL
- **Latência:** 339.83ms
- **Detalhes:** Expected 200, got 401

### Security - Webhook sem Assinatura (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 187.09ms
- **Detalhes:** Status 401

### Security - Webhook com Assinatura Inválida (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 355.3ms
- **Detalhes:** Status 401

### Blockchain - Verificar Documento

- **Status:** ❌ FAIL
- **Latência:** 6253.87ms
- **Detalhes:** Expected 200, got 500

### Blockchain - Registrar Assinatura

- **Status:** ❌ FAIL
- **Latência:** 6193.24ms
- **Detalhes:** Expected 200, got 500

### Blockchain - Mint Identity

- **Status:** ❌ FAIL
- **Latência:** 311.75ms
- **Detalhes:** Expected 200, got 400

### Failsafe - Ativar Botão de Pânico

- **Status:** ✅ PASS
- **Latência:** 503.35ms
- **Detalhes:** Status 200

### Failsafe - Pânico sem Autenticação (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 212.56ms
- **Detalhes:** Status 401

### Failsafe - Pânico com Dados Parciais

- **Status:** ✅ PASS
- **Latência:** 353.14ms
- **Detalhes:** Status 200

### Security - SQL Injection (deve falhar)

- **Status:** ❌ FAIL
- **Latência:** 183.19ms
- **Detalhes:** Expected 401, got 400

### Security - XSS no Email (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 188.82ms
- **Detalhes:** Status 400

### Security - Registro sem Senha (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 202.63ms
- **Detalhes:** Status 400

### Security - Login sem Email (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 346.26ms
- **Detalhes:** Status 400

### Frontend - Página Inicial

- **Status:** ✅ PASS
- **Latência:** 195.27ms
- **Detalhes:** HTML carregado

### Frontend - Asset /assets/index.css

- **Status:** ⚠️ WARN
- **Latência:** 216.59ms
- **Detalhes:** Status 404

### Frontend - Asset /assets/index.js

- **Status:** ⚠️ WARN
- **Latência:** 185.2ms
- **Detalhes:** Status 404

### Frontend - Logo

- **Status:** ⚠️ WARN
- **Latência:** 192.87ms
- **Detalhes:** Status 404

