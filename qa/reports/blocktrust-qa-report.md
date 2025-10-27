# Relatório de QA - BTS Blocktrust

**Data:** 2025-10-27T17:13:08.262682

## Resumo Executivo

- **Total de Testes:** 26
- **✅ Passaram:** 22
- **❌ Falharam:** 1
- **⚠️ Avisos:** 3
- **Taxa de Sucesso:** 84.6%

## Latência Média por Módulo

| Módulo | Latência Média | Status |
|--------|----------------|--------|
| Backend | 580.70ms | ⚠️ Alto |
| Auth | 574.62ms | ⚠️ Alto |
| KYC | 286.23ms | ✅ OK |
| Security | 196.40ms | ✅ OK |
| Blockchain | 6371.53ms | ⚠️ Alto |
| Failsafe | 343.31ms | ✅ OK |
| Frontend | 201.96ms | ✅ OK |

## Detalhes dos Testes

### Backend - Health Check

- **Status:** ✅ PASS
- **Latência:** 580.7ms
- **Detalhes:** Status 200

### Auth - Registro de Usuário

- **Status:** ✅ PASS
- **Latência:** 727.93ms
- **Detalhes:** Status 201

### Auth - Login de Usuário

- **Status:** ✅ PASS
- **Latência:** 655.44ms
- **Detalhes:** Status 200

### Auth - Login Inválido (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 775.32ms
- **Detalhes:** Status 401

### Auth - Acesso sem Token (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 366.94ms
- **Detalhes:** Status 401

### Auth - Token Inválido (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 347.48ms
- **Detalhes:** Status 401

### KYC - Inicializar KYC

- **Status:** ✅ PASS
- **Latência:** 487.69ms
- **Detalhes:** Status 200

### KYC - Consultar Status KYC

- **Status:** ✅ PASS
- **Latência:** 201.08ms
- **Detalhes:** Status 200

### KYC - Consultar Liveness Status

- **Status:** ✅ PASS
- **Latência:** 259.74ms
- **Detalhes:** Status 200

### KYC - Webhook Sumsub (simulado)

- **Status:** ❌ FAIL
- **Latência:** 196.39ms
- **Detalhes:** Expected [200], got 401

### Security - Webhook sem Assinatura (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 189.13ms
- **Detalhes:** Status 401

### Security - Webhook com Assinatura Inválida (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 196.93ms
- **Detalhes:** Status 401

### Blockchain - Verificar Documento

- **Status:** ✅ PASS
- **Latência:** 6400.3ms
- **Detalhes:** Status 200

### Blockchain - Registrar Assinatura

- **Status:** ✅ PASS
- **Latência:** 6458.41ms
- **Detalhes:** Status 200

### Blockchain - Mint Identity

- **Status:** ✅ PASS
- **Latência:** 6255.89ms
- **Detalhes:** Status 200

### Failsafe - Ativar Botão de Pânico

- **Status:** ✅ PASS
- **Latência:** 367.55ms
- **Detalhes:** Status 200

### Failsafe - Pânico sem Autenticação (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 213.73ms
- **Detalhes:** Status 401

### Failsafe - Pânico com Dados Parciais

- **Status:** ✅ PASS
- **Latência:** 448.64ms
- **Detalhes:** Status 200

### Security - SQL Injection (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 213.23ms
- **Detalhes:** Status 400

### Security - XSS no Email (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 183.83ms
- **Detalhes:** Status 400

### Security - Registro sem Senha (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 200.08ms
- **Detalhes:** Status 400

### Security - Login sem Email (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 195.21ms
- **Detalhes:** Status 400

### Frontend - Página Inicial

- **Status:** ✅ PASS
- **Latência:** 181.82ms
- **Detalhes:** HTML carregado

### Frontend - Asset /assets/index.css

- **Status:** ⚠️ WARN
- **Latência:** 224.35ms
- **Detalhes:** Status 404

### Frontend - Asset /assets/index.js

- **Status:** ⚠️ WARN
- **Latência:** 185.24ms
- **Detalhes:** Status 404

### Frontend - Logo

- **Status:** ⚠️ WARN
- **Latência:** 216.44ms
- **Detalhes:** Status 404

