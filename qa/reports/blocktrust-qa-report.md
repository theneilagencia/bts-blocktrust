# Relatório de QA - BTS Blocktrust

**Data:** 2025-10-27T17:31:14.786946

## Resumo Executivo

- **Total de Testes:** 26
- **✅ Passaram:** 25
- **❌ Falharam:** 1
- **⚠️ Avisos:** 0
- **Taxa de Sucesso:** 96.2%

## Latência Média por Módulo

| Módulo | Latência Média | Status |
|--------|----------------|--------|
| Backend | 477.13ms | ✅ OK |
| Auth | 493.29ms | ✅ OK |
| KYC | 423.52ms | ✅ OK |
| Security | 257.13ms | ✅ OK |
| Blockchain | 6309.72ms | ⚠️ Alto |
| Failsafe | 312.77ms | ✅ OK |
| Frontend | 380.59ms | ✅ OK |

## Detalhes dos Testes

### Backend - Health Check

- **Status:** ✅ PASS
- **Latência:** 477.13ms
- **Detalhes:** Status 200

### Auth - Registro de Usuário

- **Status:** ✅ PASS
- **Latência:** 800.55ms
- **Detalhes:** Status 201

### Auth - Login de Usuário

- **Status:** ✅ PASS
- **Latência:** 675.95ms
- **Detalhes:** Status 200

### Auth - Login Inválido (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 598.64ms
- **Detalhes:** Status 401

### Auth - Acesso sem Token (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 212.28ms
- **Detalhes:** Status 401

### Auth - Token Inválido (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 179.01ms
- **Detalhes:** Status 401

### KYC - Inicializar KYC

- **Status:** ✅ PASS
- **Latência:** 649.42ms
- **Detalhes:** Status 200

### KYC - Consultar Status KYC

- **Status:** ✅ PASS
- **Latência:** 405.89ms
- **Detalhes:** Status 200

### KYC - Consultar Liveness Status

- **Status:** ✅ PASS
- **Latência:** 256.5ms
- **Detalhes:** Status 200

### KYC - Webhook Sumsub (simulado)

- **Status:** ❌ FAIL
- **Latência:** 382.29ms
- **Detalhes:** Expected [200], got 401

### Security - Webhook sem Assinatura (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 184.29ms
- **Detalhes:** Status 401

### Security - Webhook com Assinatura Inválida (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 348.14ms
- **Detalhes:** Status 401

### Blockchain - Verificar Documento

- **Status:** ✅ PASS
- **Latência:** 6236.93ms
- **Detalhes:** Status 200

### Blockchain - Registrar Assinatura

- **Status:** ✅ PASS
- **Latência:** 6446.06ms
- **Detalhes:** Status 200

### Blockchain - Mint Identity

- **Status:** ✅ PASS
- **Latência:** 6246.19ms
- **Detalhes:** Status 200

### Failsafe - Ativar Botão de Pânico

- **Status:** ✅ PASS
- **Latência:** 474.36ms
- **Detalhes:** Status 200

### Failsafe - Pânico sem Autenticação (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 188.22ms
- **Detalhes:** Status 401

### Failsafe - Pânico com Dados Parciais

- **Status:** ✅ PASS
- **Latência:** 275.73ms
- **Detalhes:** Status 200

### Security - SQL Injection (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 454.85ms
- **Detalhes:** Status 400

### Security - XSS no Email (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 182.34ms
- **Detalhes:** Status 400

### Security - Registro sem Senha (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 167.34ms
- **Detalhes:** Status 400

### Security - Login sem Email (deve falhar)

- **Status:** ✅ PASS
- **Latência:** 205.81ms
- **Detalhes:** Status 400

### Frontend - Página Inicial

- **Status:** ✅ PASS
- **Latência:** 182.25ms
- **Detalhes:** HTML carregado

### Frontend - Asset CSS

- **Status:** ✅ PASS
- **Latência:** 323.25ms
- **Detalhes:** Carregado: /assets/index-DLGOwAYe.css

### Frontend - Asset JS

- **Status:** ✅ PASS
- **Latência:** 747.22ms
- **Detalhes:** Carregado: /assets/index-DUx0o7Ww.js

### Frontend - Logo

- **Status:** ✅ PASS
- **Latência:** 269.66ms
- **Detalhes:** Imagem carregada: /logo.png

