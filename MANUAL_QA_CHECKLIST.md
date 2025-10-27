# Roteiro de Testes Manuais - BTS Blocktrust

**Versão:** 1.0  
**Data:** 27 de Outubro de 2025  
**Autor:** Manus AI  
**Ambiente de Teste:** [https://bts-blocktrust.onrender.com](https://bts-blocktrust.onrender.com)

---

## Objetivo

Gerar um **roteiro de testes manuais** (manual QA checklist) para validar **todas as funcionalidades críticas** da plataforma **BTS Blocktrust**, incluindo:

- Login e autenticação JWT
- Upload e geração de hash de documento
- Registro do hash na blockchain (Polygon)
- Verificação visual de retorno (UI e toasts)
- Integração KYC e Liveness com Sumsub
- Webhook e atualização de status
- Segurança e restrições de acesso

---

## Estrutura Esperada do Roteiro

O roteiro deve ser dividido em **7 seções principais**, cada uma com:

1. **Objetivo do teste**
2. **Pré-requisitos**
3. **Passos a passar (para execução manual)**
4. **Resultado esperado**
5. **Critério de aprovação (PASS/FAIL)**

---

## 📋 Seção 1: Login e Autenticação

### Objetivo do Teste
Verificar login válido, inválido e expiração de sessão.

### Pré-requisitos
- Acesso à URL da aplicação: [https://bts-blocktrust.onrender.com](https://bts-blocktrust.onrender.com)
- Usuário de teste registrado no sistema
- Navegador atualizado (Chrome, Firefox, Edge)

### Passos para Execução Manual

#### Teste 1.1: Login com credenciais válidas
1. Acessar a página inicial da aplicação
2. Clicar no botão "Login" ou navegar para `/login`
3. Inserir email válido: `teste@blocktrust.com`
4. Inserir senha válida: `Senha@123`
5. Clicar no botão "Entrar"

**Resultado Esperado:**
- Redirecionamento para o dashboard do usuário
- Token JWT armazenado no localStorage
- Mensagem de boas-vindas exibida
- Menu de navegação visível com opções do usuário

**Critério de Aprovação:** ✅ PASS se o login for bem-sucedido e o dashboard for exibido. ❌ FAIL se houver erro ou redirecionamento incorreto.

---

#### Teste 1.2: Login com credenciais inválidas
1. Acessar a página de login
2. Inserir email válido: `teste@blocktrust.com`
3. Inserir senha **inválida**: `SenhaErrada123`
4. Clicar no botão "Entrar"

**Resultado Esperado:**
- Mensagem de erro exibida: "Email ou senha inválidos"
- Usuário permanece na página de login
- Nenhum token JWT armazenado

**Critério de Aprovação:** ✅ PASS se a mensagem de erro for exibida e o acesso for negado. ❌ FAIL se o login for permitido.

---

#### Teste 1.3: Expiração de sessão
1. Fazer login com credenciais válidas
2. Aguardar o tempo de expiração do token (configurado no backend)
3. Tentar acessar uma página protegida (ex: `/dashboard`)

**Resultado Esperado:**
- Redirecionamento automático para a página de login
- Mensagem: "Sessão expirada. Faça login novamente."
- Token JWT removido do localStorage

**Critério de Aprovação:** ✅ PASS se o usuário for redirecionado e forçado a fazer login novamente. ❌ FAIL se o acesso for mantido após expiração.

---

## 📋 Seção 2: Upload de Documento e Hash

### Objetivo do Teste
Testar upload de PDF, cálculo do hash e exibição correta na interface.

### Pré-requisitos
- Usuário autenticado no sistema
- Arquivo PDF de teste disponível (tamanho < 10MB)
- Navegador com suporte a FileReader API

### Passos para Execução Manual

#### Teste 2.1: Upload de PDF válido
1. Fazer login no sistema
2. Navegar para a página de upload de documentos
3. Clicar no botão "Selecionar Arquivo" ou área de drag-and-drop
4. Selecionar um arquivo PDF válido (ex: `contrato_teste.pdf`)
5. Aguardar o cálculo do hash

**Resultado Esperado:**
- Arquivo carregado com sucesso
- Hash SHA-256 calculado e exibido na interface
- Hash exibido no formato hexadecimal (64 caracteres)
- Botão "Registrar na Blockchain" habilitado

**Critério de Aprovação:** ✅ PASS se o hash for calculado corretamente e exibido. ❌ FAIL se houver erro no upload ou cálculo do hash.

---

#### Teste 2.2: Upload de arquivo inválido (não-PDF)
1. Fazer login no sistema
2. Navegar para a página de upload de documentos
3. Tentar fazer upload de um arquivo que não é PDF (ex: `.jpg`, `.docx`)

**Resultado Esperado:**
- Mensagem de erro exibida: "Apenas arquivos PDF são permitidos"
- Upload bloqueado
- Nenhum hash calculado

**Critério de Aprovação:** ✅ PASS se o upload for bloqueado e a mensagem de erro for exibida. ❌ FAIL se o arquivo inválido for aceito.

---

#### Teste 2.3: Upload de arquivo muito grande
1. Fazer login no sistema
2. Navegar para a página de upload de documentos
3. Tentar fazer upload de um arquivo PDF > 10MB

**Resultado Esperado:**
- Mensagem de erro exibida: "Arquivo muito grande. Tamanho máximo: 10MB"
- Upload bloqueado

**Critério de Aprovação:** ✅ PASS se o upload for bloqueado. ❌ FAIL se o arquivo grande for aceito.

---

## 📋 Seção 3: Registro na Blockchain

### Objetivo do Teste
Validar o envio do hash para registro, checar o retorno da transação e toast de sucesso.

### Pré-requisitos
- Usuário autenticado
- Documento com hash calculado
- Integração com Toolblox configurada (ou modo mock ativo)

### Passos para Execução Manual

#### Teste 3.1: Registro de hash na blockchain (sucesso)
1. Fazer login no sistema
2. Fazer upload de um PDF válido
3. Aguardar o cálculo do hash
4. Clicar no botão "Registrar na Blockchain"
5. Aguardar a resposta da API

**Resultado Esperado:**
- Toast de sucesso exibido: "Documento registrado na blockchain com sucesso!"
- ID da transação exibido na interface
- Link para visualizar a transação no Polygon Explorer
- Status do documento atualizado para "Registrado"

**Critério de Aprovação:** ✅ PASS se o registro for bem-sucedido e o toast for exibido. ❌ FAIL se houver erro ou timeout.

---

#### Teste 3.2: Registro de hash duplicado
1. Fazer login no sistema
2. Fazer upload do mesmo PDF já registrado anteriormente
3. Tentar registrar novamente na blockchain

**Resultado Esperado:**
- Mensagem de aviso: "Este documento já foi registrado anteriormente"
- Exibição do ID da transação anterior
- Opção de visualizar o registro existente

**Critério de Aprovação:** ✅ PASS se a duplicação for detectada e o aviso exibido. ❌ FAIL se permitir registro duplicado.

---

#### Teste 3.3: Falha na comunicação com a blockchain
1. Fazer login no sistema
2. Fazer upload de um PDF válido
3. Simular falha na API (desconectar internet ou usar modo mock com erro)
4. Tentar registrar na blockchain

**Resultado Esperado:**
- Toast de erro exibido: "Erro ao registrar na blockchain. Tente novamente."
- Botão "Tentar Novamente" disponível
- Documento permanece com status "Pendente"

**Critério de Aprovação:** ✅ PASS se o erro for tratado corretamente. ❌ FAIL se a aplicação travar ou não exibir mensagem de erro.

---

## 📋 Seção 4: KYC e Verificação Sumsub

### Objetivo do Teste
Iniciar verificação, enviar documento, fazer selfie (liveness) e verificar status "Aprovado".

### Pré-requisitos
- Usuário autenticado
- Integração com Sumsub configurada (ou modo mock ativo)
- Documento de identidade válido (RG, CNH, Passaporte)
- Webcam funcional para selfie

### Passos para Execução Manual

#### Teste 4.1: Iniciar verificação KYC
1. Fazer login no sistema
2. Navegar para a página de verificação KYC
3. Clicar no botão "Iniciar Verificação"
4. Aguardar o carregamento do SDK do Sumsub

**Resultado Esperado:**
- SDK do Sumsub carregado na interface
- Instruções de verificação exibidas
- Opção de selecionar tipo de documento (RG, CNH, Passaporte)

**Critério de Aprovação:** ✅ PASS se o SDK for carregado corretamente. ❌ FAIL se houver erro no carregamento.

---

#### Teste 4.2: Enviar documento de identidade
1. Iniciar verificação KYC
2. Selecionar tipo de documento: "CNH"
3. Fazer upload da foto da frente da CNH
4. Fazer upload da foto do verso da CNH
5. Confirmar envio

**Resultado Esperado:**
- Documentos enviados com sucesso
- Mensagem: "Documentos recebidos. Aguarde a análise."
- Progresso da verificação atualizado (ex: "50% concluído")

**Critério de Aprovação:** ✅ PASS se os documentos forem enviados e aceitos. ❌ FAIL se houver erro no upload.

---

#### Teste 4.3: Fazer selfie (liveness)
1. Completar o envio de documentos
2. Seguir para a etapa de liveness
3. Permitir acesso à webcam
4. Seguir as instruções na tela (virar o rosto, piscar, etc.)
5. Confirmar a selfie

**Resultado Esperado:**
- Selfie capturada com sucesso
- Mensagem: "Verificação de liveness concluída"
- Progresso atualizado para "100% concluído"
- Status KYC: "Em análise"

**Critério de Aprovação:** ✅ PASS se a selfie for capturada e aceita. ❌ FAIL se houver erro na captura ou validação.

---

#### Teste 4.4: Verificar status "Aprovado"
1. Completar todas as etapas do KYC
2. Aguardar a análise do Sumsub (ou simular aprovação em modo mock)
3. Atualizar a página ou aguardar webhook
4. Verificar o status do KYC no dashboard

**Resultado Esperado:**
- Status KYC atualizado para "Aprovado"
- Badge verde exibido ao lado do nome do usuário
- Acesso liberado para funcionalidades restritas

**Critério de Aprovação:** ✅ PASS se o status for atualizado corretamente. ❌ FAIL se o status não for atualizado ou estiver incorreto.

---

## 📋 Seção 5: Webhook e Atualização de Status

### Objetivo do Teste
Simular webhook do Sumsub e confirmar atualização automática no painel do usuário.

### Pré-requisitos
- Usuário com KYC em análise
- Acesso ao endpoint de webhook: `/api/kyc/webhook`
- Ferramenta para simular requisições HTTP (Postman, cURL, ou script Python)

### Passos para Execução Manual

#### Teste 5.1: Simular webhook de aprovação
1. Obter o ID do usuário e applicant ID do Sumsub
2. Enviar requisição POST para `/api/kyc/webhook` com payload:
   ```json
   {
     "type": "applicantReviewed",
     "applicantId": "test_applicant_123",
     "externalUserId": "1",
     "reviewStatus": "completed",
     "reviewResult": {
       "reviewAnswer": "GREEN"
     }
   }
   ```
3. Incluir header `X-Payload-Digest` com assinatura HMAC (ou usar modo mock)
4. Verificar resposta da API

**Resultado Esperado:**
- Resposta HTTP 200 OK
- Status do usuário atualizado no banco de dados para "Aprovado"
- Webhook processado com sucesso

**Critério de Aprovação:** ✅ PASS se o webhook for processado e o status atualizado. ❌ FAIL se houver erro 401 ou 500.

---

#### Teste 5.2: Verificar atualização automática no painel
1. Após enviar o webhook de aprovação
2. Fazer login como o usuário afetado
3. Navegar para o dashboard
4. Verificar o status do KYC

**Resultado Esperado:**
- Status KYC exibido como "Aprovado"
- Badge verde visível
- Mensagem de boas-vindas: "Sua conta foi verificada!"

**Critério de Aprovação:** ✅ PASS se a atualização for refletida na interface. ❌ FAIL se o status não for atualizado automaticamente.

---

## 📋 Seção 6: Segurança e Restrições

### Objetivo do Teste
Verificar que usuários não logados ou sem KYC aprovado não conseguem registrar documentos.

### Pré-requisitos
- Navegador em modo anônimo (sem cookies/sessão)
- Usuário sem KYC aprovado

### Passos para Execução Manual

#### Teste 6.1: Acesso sem autenticação
1. Abrir navegador em modo anônimo
2. Tentar acessar diretamente a URL: `/dashboard`
3. Verificar redirecionamento

**Resultado Esperado:**
- Redirecionamento automático para `/login`
- Mensagem: "Você precisa fazer login para acessar esta página"
- Nenhum conteúdo do dashboard exibido

**Critério de Aprovação:** ✅ PASS se o acesso for bloqueado e o redirecionamento ocorrer. ❌ FAIL se o dashboard for acessível sem login.

---

#### Teste 6.2: Registro de documento sem KYC aprovado
1. Fazer login com usuário que **não** tem KYC aprovado
2. Tentar acessar a página de upload de documentos
3. Tentar fazer upload de um PDF

**Resultado Esperado:**
- Mensagem de aviso: "Complete a verificação KYC para registrar documentos"
- Botão "Registrar na Blockchain" desabilitado
- Link para iniciar KYC exibido

**Critério de Aprovação:** ✅ PASS se o registro for bloqueado. ❌ FAIL se usuário sem KYC conseguir registrar documentos.

---

#### Teste 6.3: Proteção contra SQL Injection
1. Acessar a página de login
2. No campo de email, inserir: `' OR '1'='1' --`
3. No campo de senha, inserir qualquer valor
4. Tentar fazer login

**Resultado Esperado:**
- Login bloqueado
- Mensagem de erro: "Email ou senha inválidos"
- Nenhum acesso concedido

**Critério de Aprovação:** ✅ PASS se o ataque for bloqueado. ❌ FAIL se o login for bem-sucedido.

---

#### Teste 6.4: Proteção contra XSS
1. Acessar a página de registro
2. No campo de nome, inserir: `<script>alert('XSS')</script>`
3. Completar o registro
4. Verificar se o script é executado

**Resultado Esperado:**
- Script não executado
- Nome armazenado como texto puro (escaped)
- Nenhum alerta JavaScript exibido

**Critério de Aprovação:** ✅ PASS se o XSS for bloqueado. ❌ FAIL se o script for executado.

---

## 📋 Seção 7: UX/UI e Acessibilidade

### Objetivo do Teste
Validar mensagens de erro e tempo de resposta da interface.

### Pré-requisitos
- Navegador atualizado
- Conexão de internet estável
- Ferramenta de medição de performance (DevTools)

### Passos para Execução Manual

#### Teste 7.1: Mensagens de erro claras
1. Fazer login com credenciais inválidas
2. Verificar a mensagem de erro exibida
3. Tentar fazer upload de arquivo inválido
4. Verificar a mensagem de erro exibida

**Resultado Esperado:**
- Mensagens de erro claras e específicas
- Sem mensagens técnicas ou códigos de erro expostos
- Instruções de como corrigir o erro

**Critério de Aprovação:** ✅ PASS se as mensagens forem claras e úteis. ❌ FAIL se as mensagens forem genéricas ou confusas.

---

#### Teste 7.2: Tempo de resposta da interface
1. Fazer login no sistema
2. Navegar entre diferentes páginas (dashboard, upload, KYC)
3. Medir o tempo de carregamento de cada página usando DevTools

**Resultado Esperado:**
- Tempo de carregamento < 2 segundos para páginas principais
- Feedback visual durante carregamento (spinner, skeleton)
- Nenhuma tela em branco ou travamento

**Critério de Aprovação:** ✅ PASS se o tempo de resposta for aceitável (< 2s). ❌ FAIL se houver lentidão ou travamento.

---

#### Teste 7.3: Responsividade mobile
1. Acessar a aplicação em dispositivo mobile ou usar DevTools (modo mobile)
2. Testar todas as funcionalidades principais
3. Verificar layout e usabilidade

**Resultado Esperado:**
- Layout adaptado para tela pequena
- Botões e campos clicáveis sem zoom
- Menu de navegação funcional
- Todas as funcionalidades acessíveis

**Critério de Aprovação:** ✅ PASS se a aplicação for totalmente funcional em mobile. ❌ FAIL se houver problemas de layout ou usabilidade.

---

## 📊 Resumo de Aprovação

Para que a aplicação seja **aprovada em QA manual**, todos os testes devem resultar em **PASS**. Caso algum teste resulte em **FAIL**, a funcionalidade correspondente deve ser corrigida antes do deploy em produção.

| Seção | Total de Testes | Critério de Aprovação |
| ----- | --------------- | --------------------- |
| 1. Login e Autenticação | 3 | 3/3 PASS |
| 2. Upload de Documento e Hash | 3 | 3/3 PASS |
| 3. Registro na Blockchain | 3 | 3/3 PASS |
| 4. KYC e Verificação Sumsub | 4 | 4/4 PASS |
| 5. Webhook e Atualização de Status | 2 | 2/2 PASS |
| 6. Segurança e Restrições | 4 | 4/4 PASS |
| 7. UX/UI e Acessibilidade | 3 | 3/3 PASS |
| **TOTAL** | **22** | **22/22 PASS** |

---

**Status Final:** ✅ **APROVADO PARA PRODUÇÃO** se todos os testes passarem.

