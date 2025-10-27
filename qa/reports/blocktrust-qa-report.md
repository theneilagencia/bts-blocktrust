# Relatório de QA - BTS Blocktrust

**Data:** 2025-10-27T16:49:17.309819

## Resumo Executivo

- **Total de Testes:** 26
- **✅ Passaram:** 18
- **❌ Falharam:** 5
- **⚠️ Avisos:** 3
- **Taxa de Sucesso:** 69.2%

## Latência Média por Módulo

| Módulo | Latência Média | Status |
|--------|----------------|--------|
| Backend | 190.71ms | ✅ OK |
| Auth | 512.85ms | ⚠️ Alto |
| KYC | 297.37ms | ✅ OK |
| Security | 230.57ms | ✅ OK |
| Blockchain | 4212.09ms | ⚠️ Alto |
| Failsafe | 419.21ms | ✅ OK |
| Frontend | 251.59ms | ✅ OK |

## Detalhes dos Testes

### Backend - Health Check

- **Status:** ✅ PASS
- **Latência:** 190.71ms
- **Detalhes:** Status 200

### Auth - Registro de Usuário

- **Status:** ✅ PASS
- **Latência:** 642.77ms
- **Detalhes:** Status 201

### Auth - Login de Usuário

- **Status:** ✅ PASS
- **Latência:** 678.42ms
- **Detalhes:** Status 200

### Auth - Login Inválido (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 700.59ms
- **Detalhes:** Status 401

### Auth - Acesso sem Token (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 193.18ms
- **Detalhes:** Status 401

### Auth - Token Inválido (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 349.27ms
- **Detalhes:** Status 401

### KYC - Inicializar KYC

- **Status:** ❌ FAIL
- **Latência:** 473.87ms
- **Detalhes:** Expected [200], got 500

### KYC - Consultar Status KYC

- **Status:** ✅ PASS
- **Latência:** 189.66ms
- **Detalhes:** Status 200

### KYC - Consultar Liveness Status

- **Status:** ✅ PASS
- **Latência:** 188.65ms
- **Detalhes:** Status 200

### KYC - Webhook Sumsub (simulado)

- **Status:** ❌ FAIL
- **Latência:** 337.31ms
- **Detalhes:** Expected [200], got 401

### Security - Webhook sem Assinatura (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 190.15ms
- **Detalhes:** Status 401

### Security - Webhook com Assinatura Inválida (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 220.52ms
- **Detalhes:** Status 401

### Blockchain - Verificar Documento

- **Status:** ❌ FAIL
- **Latência:** 6233.18ms
- **Detalhes:** Expected [200], got 500

### Blockchain - Registrar Assinatura

- **Status:** ❌ FAIL
- **Latência:** 6210.02ms
- **Detalhes:** Expected [200], got 500

### Blockchain - Mint Identity

- **Status:** ❌ FAIL
- **Latência:** 193.08ms
- **Detalhes:** Expected [200], got 400

### Failsafe - Ativar Botão de Pânico

- **Status:** ✅ PASS
- **Latência:** 301.24ms
- **Detalhes:** Status 200

### Failsafe - Pânico sem Autenticação (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 482.96ms
- **Detalhes:** Status 401

### Failsafe - Pânico com Dados Parciais

- **Status:** ✅ PASS
- **Latência:** 473.43ms
- **Detalhes:** Status 200

### Security - SQL Injection (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 350.22ms
- **Detalhes:** Status 400

### Security - XSS no Email (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 199.74ms
- **Detalhes:** Status 400

### Security - Registro sem Senha (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 205.32ms
- **Detalhes:** Status 400

### Security - Login sem Email (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 217.49ms
- **Detalhes:** Status 400

### Frontend - Página Inicial

- **Status:** ✅ PASS
- **Latência:** 219.73ms
- **Detalhes:** HTML carregado

### Frontend - Asset /assets/index.css

- **Status:** ⚠️ WARN
- **Latência:** 196.22ms
- **Detalhes:** Status 404

### Frontend - Asset /assets/index.js

- **Status:** ⚠️ WARN
- **Latência:** 224.45ms
- **Detalhes:** Status 404

### Frontend - Logo

- **Status:** ⚠️ WARN
- **Latência:** 365.97ms
- **Detalhes:** Status 404

