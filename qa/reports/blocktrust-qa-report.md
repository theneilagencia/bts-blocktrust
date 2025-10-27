# Relatório de QA - BTS Blocktrust

**Data:** 2025-10-27T17:08:39.707026

## Resumo Executivo

- **Total de Testes:** 26
- **✅ Passaram:** 22
- **❌ Falharam:** 1
- **⚠️ Avisos:** 3
- **Taxa de Sucesso:** 84.6%

## Latência Média por Módulo

| Módulo | Latência Média | Status |
|--------|----------------|--------|
| Backend | 194.53ms | ✅ OK |
| Auth | 479.33ms | ✅ OK |
| KYC | 373.90ms | ✅ OK |
| Security | 256.55ms | ✅ OK |
| Blockchain | 6368.83ms | ⚠️ Alto |
| Failsafe | 283.18ms | ✅ OK |
| Frontend | 207.66ms | ✅ OK |

## Detalhes dos Testes

### Backend - Health Check

- **Status:** ✅ PASS
- **Latência:** 194.53ms
- **Detalhes:** Status 200

### Auth - Registro de Usuário

- **Status:** ✅ PASS
- **Latência:** 681.93ms
- **Detalhes:** Status 201

### Auth - Login de Usuário

- **Status:** ✅ PASS
- **Latência:** 645.82ms
- **Detalhes:** Status 200

### Auth - Login Inválido (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 664.82ms
- **Detalhes:** Status 401

### Auth - Acesso sem Token (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 194.98ms
- **Detalhes:** Status 401

### Auth - Token Inválido (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 209.12ms
- **Detalhes:** Status 401

### KYC - Inicializar KYC

- **Status:** ✅ PASS
- **Latência:** 487.01ms
- **Detalhes:** Status 200

### KYC - Consultar Status KYC

- **Status:** ✅ PASS
- **Latência:** 599.81ms
- **Detalhes:** Status 200

### KYC - Consultar Liveness Status

- **Status:** ✅ PASS
- **Latência:** 192.15ms
- **Detalhes:** Status 200

### KYC - Webhook Sumsub (simulado)

- **Status:** ❌ FAIL
- **Latência:** 216.64ms
- **Detalhes:** Expected [200], got 401

### Security - Webhook sem Assinatura (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 172.44ms
- **Detalhes:** Status 401

### Security - Webhook com Assinatura Inválida (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 369.72ms
- **Detalhes:** Status 401

### Blockchain - Verificar Documento

- **Status:** ✅ PASS
- **Latência:** 6467.06ms
- **Detalhes:** Status 200

### Blockchain - Registrar Assinatura

- **Status:** ✅ PASS
- **Latência:** 6222.48ms
- **Detalhes:** Status 200

### Blockchain - Mint Identity

- **Status:** ✅ PASS
- **Latência:** 6416.97ms
- **Detalhes:** Status 200

### Failsafe - Ativar Botão de Pânico

- **Status:** ✅ PASS
- **Latência:** 289.02ms
- **Detalhes:** Status 200

### Failsafe - Pânico sem Autenticação (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 199.69ms
- **Detalhes:** Status 401

### Failsafe - Pânico com Dados Parciais

- **Status:** ✅ PASS
- **Latência:** 360.85ms
- **Detalhes:** Status 200

### Security - SQL Injection (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 289.94ms
- **Detalhes:** Status 400

### Security - XSS no Email (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 232.8ms
- **Detalhes:** Status 400

### Security - Registro sem Senha (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 289.1ms
- **Detalhes:** Status 400

### Security - Login sem Email (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 185.27ms
- **Detalhes:** Status 400

### Frontend - Página Inicial

- **Status:** ✅ PASS
- **Latência:** 230.12ms
- **Detalhes:** HTML carregado

### Frontend - Asset /assets/index.css

- **Status:** ⚠️ WARN
- **Latência:** 196.29ms
- **Detalhes:** Status 404

### Frontend - Asset /assets/index.js

- **Status:** ⚠️ WARN
- **Latência:** 178.13ms
- **Detalhes:** Status 404

### Frontend - Logo

- **Status:** ⚠️ WARN
- **Latência:** 226.12ms
- **Detalhes:** Status 404

