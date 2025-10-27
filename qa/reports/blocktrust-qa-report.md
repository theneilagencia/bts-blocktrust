# Relatório de QA - BTS Blocktrust

**Data:** 2025-10-27T11:48:06.037602

## Resumo Executivo

- **Total de Testes:** 26
- **✅ Passaram:** 15
- **❌ Falharam:** 8
- **⚠️ Avisos:** 3
- **Taxa de Sucesso:** 57.7%

## Latência Média por Módulo

| Módulo | Latência Média | Status |
|--------|----------------|--------|
| Backend | 210.28ms | ✅ OK |
| Auth | 526.99ms | ⚠️ Alto |
| KYC | 209.56ms | ✅ OK |
| Security | 211.32ms | ✅ OK |
| Blockchain | 4263.30ms | ⚠️ Alto |
| Failsafe | 320.81ms | ✅ OK |
| Frontend | 179.08ms | ✅ OK |

## Detalhes dos Testes

### Backend - Health Check

- **Status:** ✅ PASS
- **Latência:** 210.28ms
- **Detalhes:** Status 200

### Auth - Registro de Usuário

- **Status:** ✅ PASS
- **Latência:** 716.91ms
- **Detalhes:** Status 201

### Auth - Login de Usuário

- **Status:** ✅ PASS
- **Latência:** 681.11ms
- **Detalhes:** Status 200

### Auth - Login Inválido (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 693.98ms
- **Detalhes:** Status 401

### Auth - Acesso sem Token (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 188.58ms
- **Detalhes:** Status 401

### Auth - Token Inválido (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 354.39ms
- **Detalhes:** Status 401

### KYC - Inicializar KYC

- **Status:** ❌ FAIL
- **Latência:** 249.34ms
- **Detalhes:** Expected 200, got 500

### KYC - Consultar Status KYC

- **Status:** ❌ FAIL
- **Latência:** 205.93ms
- **Detalhes:** Expected 200, got 500

### KYC - Consultar Liveness Status

- **Status:** ❌ FAIL
- **Latência:** 196.35ms
- **Detalhes:** Expected 200, got 500

### KYC - Webhook Sumsub (simulado)

- **Status:** ❌ FAIL
- **Latência:** 186.63ms
- **Detalhes:** Expected 200, got 401

### Security - Webhook sem Assinatura (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 168.79ms
- **Detalhes:** Status 401

### Security - Webhook com Assinatura Inválida (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 190.39ms
- **Detalhes:** Status 401

### Blockchain - Verificar Documento

- **Status:** ❌ FAIL
- **Latência:** 6422.19ms
- **Detalhes:** Expected 200, got 500

### Blockchain - Registrar Assinatura

- **Status:** ❌ FAIL
- **Latência:** 6183.51ms
- **Detalhes:** Expected 200, got 500

### Blockchain - Mint Identity

- **Status:** ❌ FAIL
- **Latência:** 184.21ms
- **Detalhes:** Expected 200, got 400

### Failsafe - Ativar Botão de Pânico

- **Status:** ✅ PASS
- **Latência:** 257.48ms
- **Detalhes:** Status 200

### Failsafe - Pânico sem Autenticação (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 236.38ms
- **Detalhes:** Status 401

### Failsafe - Pânico com Dados Parciais

- **Status:** ✅ PASS
- **Latência:** 468.56ms
- **Detalhes:** Status 200

### Security - SQL Injection (deve falhar)

- **Status:** ❌ FAIL
- **Latência:** 360.52ms
- **Detalhes:** Expected 401, got 400

### Security - XSS no Email (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 166.17ms
- **Detalhes:** Status 400

### Security - Registro sem Senha (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 198.46ms
- **Detalhes:** Status 400

### Security - Login sem Email (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 183.59ms
- **Detalhes:** Status 400

### Frontend - Página Inicial

- **Status:** ✅ PASS
- **Latência:** 171.72ms
- **Detalhes:** HTML carregado

### Frontend - Asset /assets/index.css

- **Status:** ⚠️ WARN
- **Latência:** 190.56ms
- **Detalhes:** Status 404

### Frontend - Asset /assets/index.js

- **Status:** ⚠️ WARN
- **Latência:** 173.64ms
- **Detalhes:** Status 404

### Frontend - Logo

- **Status:** ⚠️ WARN
- **Latência:** 180.39ms
- **Detalhes:** Status 404

