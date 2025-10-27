# Relatório de QA - BTS Blocktrust

**Data:** 2025-10-27T10:50:53.611560

## Resumo Executivo

- **Total de Testes:** 23
- **✅ Passaram:** 12
- **❌ Falharam:** 8
- **⚠️ Avisos:** 3
- **Taxa de Sucesso:** 52.2%

## Latência Média por Módulo

| Módulo | Latência Média | Status |
|--------|----------------|--------|
| Backend | 163.80ms | ✅ OK |
| Auth | 519.56ms | ⚠️ Alto |
| KYC | 239.53ms | ✅ OK |
| Security | 337.62ms | ✅ OK |
| Blockchain | 245.55ms | ✅ OK |
| Frontend | 209.50ms | ✅ OK |

## Detalhes dos Testes

### Backend - Health Check

- **Status:** ✅ PASS
- **Latência:** 163.8ms
- **Detalhes:** Status 200

### Auth - Registro de Usuário

- **Status:** ✅ PASS
- **Latência:** 664.82ms
- **Detalhes:** Status 201

### Auth - Login de Usuário

- **Status:** ✅ PASS
- **Latência:** 632.9ms
- **Detalhes:** Status 200

### Auth - Login Inválido (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 701.01ms
- **Detalhes:** Status 401

### Auth - Acesso sem Token (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 212.72ms
- **Detalhes:** Status 401

### Auth - Token Inválido (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 386.33ms
- **Detalhes:** Status 401

### KYC - Inicializar KYC

- **Status:** ❌ FAIL
- **Latência:** 192.55ms
- **Detalhes:** Expected 200, got 500

### KYC - Consultar Status KYC

- **Status:** ❌ FAIL
- **Latência:** 397.15ms
- **Detalhes:** Expected 200, got 500

### KYC - Consultar Liveness Status

- **Status:** ❌ FAIL
- **Latência:** 190.27ms
- **Detalhes:** Expected 200, got 500

### KYC - Webhook Sumsub (simulado)

- **Status:** ❌ FAIL
- **Latência:** 178.16ms
- **Detalhes:** Expected 200, got 401

### Security - Webhook sem Assinatura (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 186.82ms
- **Detalhes:** Status 401

### Security - Webhook com Assinatura Inválida (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 174.13ms
- **Detalhes:** Status 401

### Blockchain - Verificar Documento

- **Status:** ❌ FAIL
- **Latência:** 179.4ms
- **Detalhes:** Expected 200, got 400

### Blockchain - Registrar Assinatura

- **Status:** ❌ FAIL
- **Latência:** 184.44ms
- **Detalhes:** Expected 200, got 400

### Blockchain - Mint Identity

- **Status:** ❌ FAIL
- **Latência:** 372.81ms
- **Detalhes:** Expected 200, got 400

### Security - SQL Injection (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 377.94ms
- **Detalhes:** Status 401

### Security - XSS no Email (deve falhar)

- **Status:** ❌ FAIL
- **Latência:** 649.01ms
- **Detalhes:** Expected 400, got 201

### Security - Registro sem Senha (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 407.18ms
- **Detalhes:** Status 400

### Security - Login sem Email (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 230.63ms
- **Detalhes:** Status 400

### Frontend - Página Inicial

- **Status:** ✅ PASS
- **Latência:** 226.23ms
- **Detalhes:** HTML carregado

### Frontend - Asset /assets/index.css

- **Status:** ⚠️ WARN
- **Latência:** 182.24ms
- **Detalhes:** Status 404

### Frontend - Asset /assets/index.js

- **Status:** ⚠️ WARN
- **Latência:** 188.8ms
- **Detalhes:** Status 404

### Frontend - Logo

- **Status:** ⚠️ WARN
- **Latência:** 240.75ms
- **Detalhes:** Status 404

