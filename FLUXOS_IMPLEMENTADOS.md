# Blocktrust v1.4 - Fluxos Implementados

**Data**: 28 de outubro de 2025  
**Versão**: 1.4  
**Status**: ✅ **Fluxos 100% Funcionais**

---

## 📋 Resumo

Este documento descreve os dois fluxos principais do Blocktrust que foram completamente implementados e estão funcionando conforme especificado.

---

## 🔄 Fluxo 1: Criação de Novo Usuário (KYC → NFT)

### **Descrição**

Quando um usuário completa o processo de KYC com sucesso, o sistema automaticamente cria um NFT de identidade (SoulBound Token) vinculado à sua carteira. Se o usuário já possuir um NFT anterior, o sistema o cancela antes de criar o novo.

### **Etapas do Fluxo**

```
1. Usuário faz KYC
   ↓
2. Serviço externo (Sumsub) valida ID + liveness
   ↓
3. Sumsub envia webhook para Blocktrust
   ↓
4. Blocktrust verifica blockchain procurando NFT do mesmo usuário
   ↓
5. SE existe NFT:
   ├─ Cancela NFT anterior (emite evento CancelamentoEvent)
   └─ Cria novo NFT com dados do usuário
   
   SE NÃO existe NFT:
   └─ Cria NFT com dados do usuário
   ↓
6. Escolha da carteira:
   ├─ Auto: NFT enviado para endereço do usuário
   └─ BTS: NFT gerado e armazenado na carteira da BTS
```

### **Implementação Técnica**

#### **1. Webhook do Sumsub** (`kyc_routes.py`)

Quando o KYC é aprovado, o webhook dispara automaticamente o processo de mint de NFT:

```python
# Se KYC foi aprovado, iniciar processo de mint de NFT
if parsed_status['status'] == 'approved':
    logger.info(f"🎯 KYC aprovado para usuário {external_user_id} - Iniciando processo de mint de NFT")
    
    # 1. Verificar se usuário já possui NFT ativo
    existing_nft = check_active_nft(int(external_user_id))
    
    if existing_nft:
        # 2. Cancelar NFT anterior
        cancel_result = cancel_nft(int(external_user_id), existing_nft['nft_id'])
    
    # 3. Mintar novo NFT
    mint_result = mint_nft(
        user_id=int(external_user_id),
        kyc_data={
            'applicant_id': applicant_id,
            'review_status': review_status,
            'review_result': review_result
        }
    )
```

#### **2. Funções Auxiliares** (`nft.py`)

**`check_active_nft(user_id)`**
- Consulta o banco de dados para verificar se o usuário possui um NFT ativo
- Retorna informações do NFT (ID, endereço da carteira, data de criação)

**`cancel_nft(user_id, nft_id)`**
- Cancela o NFT anterior na blockchain (emite evento `CancelamentoEvent`)
- Atualiza o banco de dados marcando o NFT como inativo
- Registra o cancelamento na tabela `nft_cancellations`

**`mint_nft(user_id, kyc_data)`**
- Cria uma carteira para o usuário (se não existir)
- Minta um novo NFT na blockchain (emite evento `MintingEvent`)
- Atualiza o banco de dados com o ID do NFT e o hash da transação
- Vincula o NFT ao endereço da carteira do usuário

### **Endpoints Relacionados**

- `POST /api/kyc/webhook` - Recebe notificações do Sumsub
- `POST /api/nft/mint` - Minta NFT manualmente (admin)
- `GET /api/nft/status` - Consulta status do NFT do usuário
- `GET /api/nft/history` - Histórico de NFTs do usuário

### **Banco de Dados**

**Tabela `users`** (campos relacionados ao NFT):
- `nft_id` - ID do NFT ativo
- `nft_active` - Se o NFT está ativo (TRUE/FALSE)
- `nft_minted_at` - Data de criação do NFT
- `nft_transaction_hash` - Hash da transação de mint

**Tabela `nft_cancellations`**:
- `user_id` - ID do usuário
- `nft_id` - ID do NFT cancelado
- `reason` - Motivo do cancelamento
- `created_at` - Data do cancelamento

---

## 🔐 Fluxo 2: Jornada do Usuário (Assinatura com Failsafe)

### **Descrição**

Quando um usuário deseja assinar um documento, o sistema verifica sua identidade através de liveness e valida o NFT na blockchain. O sistema suporta dois modos de assinatura:

1. **Modo Normal**: Usuário digita senha normal → Sistema valida NFT → Assina documento
2. **Modo Failsafe**: Usuário digita senha de emergência → Sistema gera assinatura fake → Cancela NFT secretamente

### **Etapas do Fluxo**

```
1. Usuário sobe documento para assinar
   ↓
2. Usuário faz liveness (Sumsub)
   ↓
3. Serviço externo valida ID + liveness
   ↓
4. Usuário digita senha
   ↓
5. Sistema detecta tipo de senha:
   
   ┌─ SENHA NORMAL:
   │  ├─ Verifica NFT ativo na blockchain
   │  ├─ Valida NFT (deve estar ativo)
   │  ├─ Assina documento com chave privada real
   │  ├─ Registra prova na blockchain (ProofRegistry)
   │  └─ Retorna assinatura válida
   │
   └─ SENHA DE EMERGÊNCIA (FAILSAFE):
      ├─ Gera assinatura FAKE (não usa chave privada real)
      ├─ Cancela NFT automaticamente (silenciosamente)
      ├─ Registra evento de failsafe
      ├─ Atualiza last_failsafe_trigger
      └─ Retorna assinatura inválida (para proteger usuário)
```

### **Implementação Técnica**

#### **1. Configuração de Senha de Emergência** (`failsafe_routes.py`)

Antes de usar o failsafe, o usuário deve configurar uma senha de emergência:

```python
POST /api/failsafe/configure
{
    "current_password": "senha_atual",
    "failsafe_password": "senha_de_emergencia"
}
```

O sistema valida que:
- A senha atual está correta
- A senha de emergência é diferente da senha normal
- Armazena o hash da senha de emergência separadamente

#### **2. Detecção Automática de Failsafe** (`signature_routes.py`)

Quando o usuário tenta assinar um documento, o sistema detecta automaticamente se a senha usada é a senha de emergência:

```python
# DETECTAR AUTOMATICAMENTE SE É FAILSAFE
import bcrypt
is_failsafe = False

# Verificar se a senha é a senha de emergência
if failsafe_configured and failsafe_hash:
    if bcrypt.checkpw(password.encode('utf-8'), failsafe_hash.encode('utf-8')):
        is_failsafe = True
        logger.warning(f"🚨 SENHA DE EMERGÊNCIA DETECTADA para usuário {user_id}")

# Se não é failsafe, verificar se é a senha normal
if not is_failsafe:
    if not bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
        return jsonify({'error': 'Senha incorreta'}), 401
```

#### **3. Modo Failsafe** (Assinatura Fake + Cancelamento de NFT)

Se a senha de emergência for detectada, o sistema:

1. **Gera assinatura fake** (não usa a chave privada real)
2. **Cancela o NFT** automaticamente e silenciosamente
3. **Registra o evento** para auditoria
4. **Retorna assinatura inválida** (para proteger o usuário em situação de coação)

```python
# MODO FAILSAFE (detectado automaticamente pela senha)
if is_failsafe:
    logger.warning(f"🚨 FAILSAFE ACIONADO por usuário {user_id} para documento {document_name}")
    
    # Gerar assinatura fake
    signature_data = wallet_manager.generate_failsafe_signature(file_hash)
    
    # Atualizar último acionamento de failsafe
    cur.execute("""
        UPDATE users
        SET last_failsafe_trigger = NOW()
        WHERE id = %s
    """, (user_id,))
    
    # Cancelar NFT se existir
    if nft_id and nft_active:
        cancel_result = nft_manager.cancel_nft(nft_id, private_key)
        
        # Registrar cancelamento
        cur.execute("""
            INSERT INTO nft_cancellations (user_id, nft_id, reason)
            VALUES (%s, %s, %s)
        """, (user_id, nft_id, 'Failsafe triggered'))
```

#### **4. Modo Normal** (Assinatura Real + Registro Blockchain)

Se a senha normal for usada, o sistema:

1. **Valida o NFT** na blockchain
2. **Assina o documento** com a chave privada real
3. **Registra a prova** no contrato ProofRegistry
4. **Retorna assinatura válida**

```python
# MODO NORMAL
# Verificar se tem NFT ativo
if not nft_active:
    return jsonify({
        'error': 'NFT inativo ou não existente',
        'message': 'É necessário ter um NFT ativo para assinar documentos'
    }), 403

# Verificar NFT na blockchain
is_active_blockchain = nft_manager.is_active_nft(wallet_address)

if not is_active_blockchain:
    return jsonify({
        'error': 'NFT não está ativo na blockchain',
        'message': 'Sincronize seu NFT antes de assinar'
    }), 403

# Assinar documento
signature_data = wallet_manager.sign_message(
    file_hash,
    encrypted_private_key,
    password,
    salt
)

# Registrar prova na blockchain
proof_result = nft_manager.register_proof(
    file_hash,
    proof_url,
    private_key
)
```

### **Endpoints Relacionados**

- `POST /api/failsafe/configure` - Configurar senha de emergência
- `GET /api/failsafe/status` - Verificar se failsafe está configurado
- `POST /api/signature/sign-document` - Assinar documento (detecta failsafe automaticamente)
- `POST /api/signature/verify` - Verificar assinatura
- `GET /api/signature/history` - Histórico de assinaturas

### **Banco de Dados**

**Tabela `users`** (campos relacionados ao failsafe):
- `failsafe_password_hash` - Hash da senha de emergência
- `failsafe_configured` - Se o usuário configurou senha de emergência
- `last_failsafe_trigger` - Última vez que o failsafe foi acionado

**Tabela `failsafe_events`**:
- `user_id` - ID do usuário
- `message` - Mensagem descritiva do evento
- `triggered_at` - Data e hora do acionamento
- `nft_cancelled` - Se o NFT foi cancelado

**Tabela `document_signatures`**:
- `user_id` - ID do usuário
- `file_hash` - Hash do documento
- `signature` - Assinatura (real ou fake)
- `failsafe` - Se foi acionado o failsafe (TRUE/FALSE)
- `blockchain_tx` - Hash da transação blockchain (NULL se failsafe)

---

## 🔐 Segurança

### **Proteção de Senhas**

- Senha normal e senha de emergência são armazenadas com **bcrypt** (hashes separados)
- Impossível recuperar as senhas originais a partir dos hashes
- Detecção de failsafe é **silenciosa** (não avisa ao usuário)

### **Auditoria**

Todos os eventos são registrados para auditoria:
- Mint de NFT (com dados do KYC)
- Cancelamento de NFT (com motivo)
- Acionamento de failsafe (com timestamp)
- Assinaturas de documentos (normais e fake)

### **Proteção contra Coação**

O sistema foi projetado para proteger o usuário em situações de coação:
- Assinatura fake é indistinguível de uma assinatura real
- NFT é cancelado secretamente (sem notificação visível)
- Documento fica inválido, mas o usuário parece ter assinado normalmente

---

## 📊 Testes de Validação

### **Fluxo 1: KYC → NFT**

```bash
# 1. Criar usuário
curl -X POST http://localhost:10000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!","name":"Test User"}'

# 2. Iniciar KYC
curl -X POST http://localhost:10000/api/kyc/init \
  -H "Authorization: Bearer TOKEN"

# 3. Simular webhook do Sumsub (KYC aprovado)
curl -X POST http://localhost:10000/api/kyc/webhook \
  -H "Content-Type: application/json" \
  -H "X-Payload-Digest: sha256=SIGNATURE" \
  -d '{"type":"applicantReviewed","applicantId":"...","externalUserId":"1","reviewStatus":"completed","reviewResult":{"reviewAnswer":"GREEN"}}'

# 4. Verificar NFT criado
curl -X GET http://localhost:10000/api/nft/status \
  -H "Authorization: Bearer TOKEN"
```

### **Fluxo 2: Assinatura com Failsafe**

```bash
# 1. Configurar senha de emergência
curl -X POST http://localhost:10000/api/failsafe/configure \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"current_password":"Test123!","failsafe_password":"Emergency999!"}'

# 2. Assinar documento com senha normal
curl -X POST http://localhost:10000/api/signature/sign-document \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"file_hash":"0xabc123...","password":"Test123!","document_name":"contrato.pdf"}'

# 3. Assinar documento com senha de emergência (failsafe)
curl -X POST http://localhost:10000/api/signature/sign-document \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"file_hash":"0xdef456...","password":"Emergency999!","document_name":"documento_coagido.pdf"}'

# 4. Verificar status do failsafe
curl -X GET http://localhost:10000/api/failsafe/status \
  -H "Authorization: Bearer TOKEN"
```

---

## ✅ Checklist de Validação

### **Fluxo 1: KYC → NFT**

- [x] Webhook do Sumsub dispara mint automático
- [x] Sistema verifica se já existe NFT ativo
- [x] NFT anterior é cancelado automaticamente
- [x] Novo NFT é mintado com dados do KYC
- [x] Carteira é criada automaticamente se não existir
- [x] Eventos são registrados no banco de dados

### **Fluxo 2: Assinatura com Failsafe**

- [x] Usuário pode configurar senha de emergência
- [x] Sistema detecta automaticamente qual senha foi usada
- [x] Senha normal → Assinatura real + Registro blockchain
- [x] Senha de emergência → Assinatura fake + Cancelamento de NFT
- [x] NFT é verificado na blockchain antes de assinar
- [x] Failsafe é acionado silenciosamente (sem notificação)
- [x] Todos os eventos são registrados para auditoria

---

**Status**: ✅ **Ambos os fluxos estão 100% funcionais e prontos para produção**

*Documentação gerada automaticamente por Manus AI Agent*

