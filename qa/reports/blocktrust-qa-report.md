# Relatório de QA - BTS Blocktrust

**Data:** 2025-10-27T17:37:29.134823

## Resumo Executivo

- **Total de Testes:** 26
- **✅ Passaram:** 26
- **❌ Falharam:** 0
- **⚠️ Avisos:** 0
- **Taxa de Sucesso:** 100.0%

## Latência Média por Módulo

| Módulo | Latência Média | Status |
|--------|----------------|--------|
| Backend | 301.08ms | ✅ OK |
| Auth | 481.39ms | ✅ OK |
| KYC | 383.00ms | ✅ OK |
| Security | 200.88ms | ✅ OK |
| Blockchain | 6349.16ms | ⚠️ Alto |
| Failsafe | 412.93ms | ✅ OK |
| Frontend | 232.55ms | ✅ OK |

## Detalhes dos Testes

### Backend - Health Check

- **Status:** ✅ PASS
- **Latência:** 301.08ms
- **Detalhes:** Status 200

### Auth - Registro de Usuário

- **Status:** ✅ PASS
- **Latência:** 671.52ms
- **Detalhes:** Status 201

### Auth - Login de Usuário

- **Status:** ✅ PASS
- **Latência:** 728.64ms
- **Detalhes:** Status 200

### Auth - Login Inválido (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 629.44ms
- **Detalhes:** Status 401

### Auth - Acesso sem Token (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 180.86ms
- **Detalhes:** Status 401

### Auth - Token Inválido (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 196.52ms
- **Detalhes:** Status 401

### KYC - Inicializar KYC

- **Status:** ✅ PASS
- **Latência:** 459.77ms
- **Detalhes:** Status 200

### KYC - Consultar Status KYC

- **Status:** ✅ PASS
- **Latência:** 230.95ms
- **Detalhes:** Status 200

### KYC - Consultar Liveness Status

- **Status:** ✅ PASS
- **Latência:** 375.66ms
- **Detalhes:** Status 200

### KYC - Webhook Sumsub (simulado)

- **Status:** ✅ PASS
- **Latência:** 465.61ms
- **Detalhes:** Status 200

### Security - Webhook sem Assinatura (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 187.75ms
- **Detalhes:** Status 401

### Security - Webhook com Assinatura Inválida

- **Status:** ✅ PASS
- **Latência:** 254.93ms
- **Detalhes:** Status 200

### Blockchain - Verificar Documento

- **Status:** ✅ PASS
- **Latência:** 6357.88ms
- **Detalhes:** Status 200

### Blockchain - Registrar Assinatura

- **Status:** ✅ PASS
- **Latência:** 6233.76ms
- **Detalhes:** Status 200

### Blockchain - Mint Identity

- **Status:** ✅ PASS
- **Latência:** 6455.85ms
- **Detalhes:** Status 200

### Failsafe - Ativar Botão de Pânico

- **Status:** ✅ PASS
- **Latência:** 413.19ms
- **Detalhes:** Status 200

### Failsafe - Pânico sem Autenticação (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 292.76ms
- **Detalhes:** Status 401

### Failsafe - Pânico com Dados Parciais

- **Status:** ✅ PASS
- **Latência:** 532.83ms
- **Detalhes:** Status 200

### Security - SQL Injection (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 233.8ms
- **Detalhes:** Status 400

### Security - XSS no Email (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 182.38ms
- **Detalhes:** Status 400

### Security - Registro sem Senha (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 182.0ms
- **Detalhes:** Status 400

### Security - Login sem Email (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 164.43ms
- **Detalhes:** Status 400

### Frontend - Página Inicial

- **Status:** ✅ PASS
- **Latência:** 178.18ms
- **Detalhes:** HTML carregado

### Frontend - Asset CSS

- **Status:** ✅ PASS
- **Latência:** 192.61ms
- **Detalhes:** Carregado: /assets/index-DLGOwAYe.css

### Frontend - Asset JS

- **Status:** ✅ PASS
- **Latência:** 304.86ms
- **Detalhes:** Carregado: /assets/index-DUx0o7Ww.js

### Frontend - Logo

- **Status:** ✅ PASS
- **Latência:** 254.55ms
- **Detalhes:** Imagem carregada: /logo.png

