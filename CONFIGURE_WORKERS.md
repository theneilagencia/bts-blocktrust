# Guia de Configuração de Background Workers - Blocktrust v1.4

## Visão Geral

O Blocktrust v1.4 utiliza **2 background workers** que executam em processos separados do web service principal:

1. **Listener**: Monitora eventos da blockchain (NFTs mintados, assinaturas registradas, failsafe ativado)
2. **Monitor**: Verifica saúde do sistema e envia alertas

## Pré-requisitos

- ✅ Web service principal deployado e funcionando
- ✅ Banco de dados PostgreSQL configurado
- ✅ Variáveis de ambiente configuradas
- ⚠️ Smart contracts deployados (para o Listener funcionar completamente)

## Opção 1: Configuração Manual via Dashboard (Recomendado)

### Passo 1: Criar Worker "Listener"

1. Acesse o Dashboard do Render: https://dashboard.render.com/
2. Clique em "New +" → "Background Worker"
3. Conecte ao repositório: `theneilagencia/bts-blocktrust`
4. Configure:
   - **Name**: `bts-blocktrust-listener`
   - **Region**: Oregon (mesmo do web service)
   - **Branch**: `master`
   - **Build Command**: `bash build.sh`
   - **Start Command**: `cd backend && python3 listener.py`
   - **Plan**: Starter (ou Free se disponível)

5. **Variáveis de Ambiente**:
   ```
   DATABASE_URL=<copiar do web service>
   POLYGON_RPC_URL=<copiar do web service>
   LISTENER_POLL_INTERVAL=15
   ```

6. Clique em "Create Background Worker"

### Passo 2: Criar Worker "Monitor"

1. Clique em "New +" → "Background Worker"
2. Conecte ao repositório: `theneilagencia/bts-blocktrust`
3. Configure:
   - **Name**: `bts-blocktrust-monitor`
   - **Region**: Oregon (mesmo do web service)
   - **Branch**: `master`
   - **Build Command**: `bash build.sh`
   - **Start Command**: `cd backend && python3 -m monitor.runner`
   - **Plan**: Starter (ou Free se disponível)

4. **Variáveis de Ambiente**:
   ```
   DATABASE_URL=<copiar do web service>
   MONITOR_CHECK_INTERVAL=60
   SLO_UPTIME_TARGET=99.5
   SLO_LATENCY_MS=800
   ALERT_WEBHOOK_URL=<opcional: webhook para alertas>
   ```

5. Clique em "Create Background Worker"

### Passo 3: Verificar Workers

Após criar os workers, verifique se estão rodando:

1. Acesse cada worker no Dashboard
2. Verifique os logs:
   - **Listener**: Deve mostrar "🎧 BLOCKTRUST BLOCKCHAIN EVENT LISTENER v1.2"
   - **Monitor**: Deve mostrar "🎯 BLOCKTRUST MONITORING SYSTEM v1.2"

3. Verifique se não há erros de conexão com o banco de dados

## Opção 2: Configuração via Blueprint (Automático)

**Nota**: Esta opção requer que você tenha acesso ao Render Blueprint. Se o `render.yaml` já está configurado, você pode usar o Blueprint para criar todos os serviços de uma vez.

### Passos:

1. Acesse: https://dashboard.render.com/
2. Clique em "New +" → "Blueprint"
3. Conecte ao repositório: `theneilagencia/bts-blocktrust`
4. O Render vai ler o `render.yaml` e criar automaticamente:
   - Web Service (bts-blocktrust)
   - Worker 1 (bts-blocktrust-listener)
   - Worker 2 (bts-blocktrust-monitor)

5. Revise as configurações e clique em "Apply"

## Configuração do Listener

### Arquivo de Configuração de Contratos

O Listener precisa de um arquivo `contracts_config.json` com os endereços e ABIs dos contratos. Este arquivo é criado automaticamente após o deploy dos smart contracts.

**Formato do arquivo**:
```json
{
  "IdentityNFT": {
    "address": "0xABC123...",
    "abi": [...]
  },
  "ProofRegistry": {
    "address": "0xDEF456...",
    "abi": [...]
  },
  "FailSafe": {
    "address": "0xGHI789...",
    "abi": [...]
  }
}
```

**Como criar o arquivo**:

1. Após fazer o deploy dos contratos (veja `DEPLOY_SMART_CONTRACTS.md`)
2. O script de deploy cria automaticamente os arquivos `.abi.json`
3. Crie o `contracts_config.json` manualmente ou use o script:

```bash
cd /home/ubuntu/bts-blocktrust
python3 -c "
import json

# Carregar endereços do .env.contracts
with open('.env.contracts', 'r') as f:
    lines = f.readlines()
    
addresses = {}
for line in lines:
    if '=' in line and not line.startswith('#'):
        key, value = line.strip().split('=')
        addresses[key] = value

# Carregar ABIs
with open('contracts/IdentityNFT.abi.json', 'r') as f:
    identity_abi = json.load(f)

with open('contracts/ProofRegistry.abi.json', 'r') as f:
    proof_abi = json.load(f)

with open('contracts/FailSafe.abi.json', 'r') as f:
    failsafe_abi = json.load(f)

# Criar contracts_config.json
config = {
    'IdentityNFT': {
        'address': addresses['IDENTITY_NFT_CONTRACT_ADDRESS'],
        'abi': identity_abi
    },
    'ProofRegistry': {
        'address': addresses['PROOF_REGISTRY_CONTRACT_ADDRESS'],
        'abi': proof_abi
    },
    'FailSafe': {
        'address': addresses['FAILSAFE_CONTRACT_ADDRESS'],
        'abi': failsafe_abi
    }
}

with open('contracts_config.json', 'w') as f:
    json.dump(config, f, indent=2)

print('✅ contracts_config.json criado com sucesso!')
"
```

4. Faça commit e push do arquivo:
```bash
git add contracts_config.json
git commit -m "feat: Adicionar configuração de contratos para Listener"
git push origin master
```

5. O Render vai fazer redeploy automático do Listener com o novo arquivo

## Configuração do Monitor

O Monitor não precisa de configuração adicional além das variáveis de ambiente. Ele vai:

1. Criar automaticamente as tabelas necessárias no banco de dados:
   - `metrics`: Armazena métricas de uptime e latência
   - `alerts`: Armazena alertas gerados

2. Executar checks a cada 60 segundos:
   - Health check da API
   - Verificação de eventos
   - Status dos contratos
   - Lag do Listener
   - Testes sintéticos

3. Gerar relatórios de SLO a cada 12 minutos

## Monitoramento dos Workers

### Logs do Listener

```
🎧 BLOCKTRUST BLOCKCHAIN EVENT LISTENER v1.2
============================================================
✅ Conectado ao Polygon Mumbai: https://polygon-mumbai.g.alchemy.com/v2/...
✅ Configuração dos contratos carregada
✅ Contratos inicializados:
  IdentityNFT:   0xABC123...
  ProofRegistry: 0xDEF456...
  FailSafe:      0xGHI789...
📍 Último bloco processado: 12345678
🎧 Iniciando listener de eventos...
🔍 Processando blocos 12345678 até 12345680...
✅ Blocos processados. Próximo: 12345681
⏳ Aguardando novos blocos... (atual: 12345681)
```

### Logs do Monitor

```
🎯 BLOCKTRUST MONITORING SYSTEM v1.2
============================================================
Check Interval: 60s
SLO Uptime Target: 99.5%
SLO Latency Target: 800ms
============================================================

🔄 Ciclo #1
🔍 Iniciando ciclo de monitoramento...
✅ api.health: 200 OK (latency: 45ms)
✅ api.events: 200 OK (latency: 120ms)
✅ api.contracts: 200 OK (latency: 89ms)
✅ listener.lag: 0 blocks behind
✅ Ciclo de monitoramento concluído
⏳ Aguardando 60s até o próximo ciclo...
```

## Troubleshooting

### Listener não inicia

**Erro**: `❌ Arquivo contracts_config.json não encontrado!`

**Solução**: 
1. Faça o deploy dos smart contracts primeiro
2. Crie o arquivo `contracts_config.json` conforme instruções acima
3. Faça commit e push do arquivo

---

**Erro**: `❌ Não foi possível conectar ao Polygon Mumbai`

**Solução**:
1. Verifique se a variável `POLYGON_RPC_URL` está configurada
2. Teste o RPC URL manualmente: `curl <RPC_URL>`
3. Tente outro provider (Alchemy, Infura, etc.)

---

### Monitor não inicia

**Erro**: `❌ Erro ao inicializar tabelas`

**Solução**:
1. Verifique se a variável `DATABASE_URL` está configurada
2. Verifique se o banco de dados está acessível
3. Verifique se as migrations foram aplicadas

---

**Erro**: `❌ Erro no ciclo de monitoramento`

**Solução**:
1. Verifique os logs detalhados do worker
2. Verifique se o web service está rodando
3. Verifique se as variáveis de ambiente estão corretas

## Custos

**Render Pricing (Starter Plan)**:
- Web Service: $7/mês
- Worker 1 (Listener): $7/mês
- Worker 2 (Monitor): $7/mês
- **Total**: $21/mês

**Alternativa Free Tier**:
- Render oferece 750 horas gratuitas por mês
- Você pode usar o Free Tier para testes
- Limite: 1 instância gratuita por serviço

## Próximos Passos

Após configurar os workers:
1. ✅ Verificar logs de cada worker
2. ✅ Testar eventos da blockchain (mint NFT, registrar assinatura)
3. ✅ Verificar métricas no banco de dados
4. ✅ Configurar alertas (webhook, email)
5. ✅ Executar testes end-to-end

## Suporte

Se encontrar problemas:
- Verifique os logs dos workers no Dashboard do Render
- Consulte a documentação do Render: https://render.com/docs
- Entre em contato com o time de desenvolvimento

---

**Versão**: 1.4  
**Data**: Outubro 2025  
**Autor**: Blocktrust Team

