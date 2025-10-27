# Relatório de QA - BTS Blocktrust

**Data:** 2025-10-27T17:26:50.117156

## Resumo Executivo

- **Total de Testes:** 26
- **✅ Passaram:** 25
- **❌ Falharam:** 1
- **⚠️ Avisos:** 0
- **Taxa de Sucesso:** 96.2%

## Latência Média por Módulo

| Módulo | Latência Média | Status |
|--------|----------------|--------|
| Backend | 209.65ms | ✅ OK |
| Auth | 549.35ms | ⚠️ Alto |
| KYC | 358.73ms | ✅ OK |
| Security | 219.85ms | ✅ OK |
| Blockchain | 6380.93ms | ⚠️ Alto |
| Failsafe | 338.40ms | ✅ OK |
| Frontend | 369.01ms | ✅ OK |

## Detalhes dos Testes

### Backend - Health Check

- **Status:** ✅ PASS
- **Latência:** 209.65ms
- **Detalhes:** Status 200

### Auth - Registro de Usuário

- **Status:** ✅ PASS
- **Latência:** 852.92ms
- **Detalhes:** Status 201

### Auth - Login de Usuário

- **Status:** ✅ PASS
- **Latência:** 820.46ms
- **Detalhes:** Status 200

### Auth - Login Inválido (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 685.13ms
- **Detalhes:** Status 401

### Auth - Acesso sem Token (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 180.75ms
- **Detalhes:** Status 401

### Auth - Token Inválido (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 207.47ms
- **Detalhes:** Status 401

### KYC - Inicializar KYC

- **Status:** ✅ PASS
- **Latência:** 562.62ms
- **Detalhes:** Status 200

### KYC - Consultar Status KYC

- **Status:** ✅ PASS
- **Latência:** 224.58ms
- **Detalhes:** Status 200

### KYC - Consultar Liveness Status

- **Status:** ✅ PASS
- **Latência:** 461.16ms
- **Detalhes:** Status 200

### KYC - Webhook Sumsub (simulado)

- **Status:** ❌ FAIL
- **Latência:** 186.57ms
- **Detalhes:** Expected [200], got 401

### Security - Webhook sem Assinatura (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 202.53ms
- **Detalhes:** Status 401

### Security - Webhook com Assinatura Inválida (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 210.23ms
- **Detalhes:** Status 401

### Blockchain - Verificar Documento

- **Status:** ✅ PASS
- **Latência:** 6219.53ms
- **Detalhes:** Status 200

### Blockchain - Registrar Assinatura

- **Status:** ✅ PASS
- **Latência:** 6399.93ms
- **Detalhes:** Status 200

### Blockchain - Mint Identity

- **Status:** ✅ PASS
- **Latência:** 6523.35ms
- **Detalhes:** Status 200

### Failsafe - Ativar Botão de Pânico

- **Status:** ✅ PASS
- **Latência:** 347.57ms
- **Detalhes:** Status 200

### Failsafe - Pânico sem Autenticação (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 343.96ms
- **Detalhes:** Status 401

### Failsafe - Pânico com Dados Parciais

- **Status:** ✅ PASS
- **Latência:** 323.66ms
- **Detalhes:** Status 200

### Security - SQL Injection (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 180.76ms
- **Detalhes:** Status 400

### Security - XSS no Email (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 359.01ms
- **Detalhes:** Status 400

### Security - Registro sem Senha (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 181.38ms
- **Detalhes:** Status 400

### Security - Login sem Email (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 185.22ms
- **Detalhes:** Status 400

### Frontend - Página Inicial

- **Status:** ✅ PASS
- **Latência:** 168.22ms
- **Detalhes:** HTML carregado

### Frontend - Asset CSS

- **Status:** ✅ PASS
- **Latência:** 177.24ms
- **Detalhes:** Carregado: /assets/index-DLGOwAYe.css

### Frontend - Asset JS

- **Status:** ✅ PASS
- **Latência:** 707.9ms
- **Detalhes:** Carregado: /assets/index-DUx0o7Ww.js

### Frontend - Logo

- **Status:** ✅ PASS
- **Latência:** 422.69ms
- **Detalhes:** Imagem carregada: /logo.png

