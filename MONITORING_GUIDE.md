# Guia de Monitoramento - Blocktrust v1.2

**Data**: 28 de outubro de 2025  
**Versão**: 1.2  
**Status**: ✅ **Pronto para Produção**

---

## 📋 Visão Geral

O sistema de monitoramento do Blocktrust v1.2 fornece **observabilidade completa** da aplicação, incluindo health checks automáticos, testes sintéticos, alertas em tempo real e métricas de SLO (Service Level Objectives).

### 🎯 Objetivos

- **Alta Disponibilidade**: Detectar e alertar sobre problemas antes que afetem os usuários
- **Performance**: Garantir que a aplicação atenda aos SLOs de latência
- **Confiabilidade**: Monitorar o listener de eventos blockchain em tempo real
- **Auditoria**: Registrar todas as métricas no banco de dados para análise histórica

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    SISTEMA DE MONITORAMENTO                  │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │ Health Checks│    │   Listener   │    │   Synthetic  │  │
│  │              │    │   Monitor    │    │    Tests     │  │
│  │  - /health   │    │              │    │              │  │
│  │  - /events   │    │  - Lag Check │    │  - Hash File │  │
│  │  - /contracts│    │  - Progress  │    │  - Wallet    │  │
│  │  - /stats    │    │              │    │  - NFT       │  │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘  │
│         │                   │                   │            │
│         └───────────────────┴───────────────────┘            │
│                             │                                │
│                    ┌────────▼────────┐                       │
│                    │   Metrics DB    │                       │
│                    │  (PostgreSQL)   │                       │
│                    └────────┬────────┘                       │
│                             │                                │
│                    ┌────────▼────────┐                       │
│                    │     Alerts      │                       │
│                    │ Slack/Telegram  │                       │
│                    └─────────────────┘                       │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚙️ Configuração

### 1. Variáveis de Ambiente

Adicione ao arquivo `.env`:

```bash
# API Base URL
API_BASE=https://bts-blocktrust.onrender.com

# Credenciais de Monitoramento
JWT_MONITOR_EMAIL=admin@bts.com
JWT_MONITOR_PASS=123

# Blockchain
POLYGON_RPC_URL=https://polygon-mumbai.infura.io/v3/SEU_INFURA_KEY

# Banco de Dados
DATABASE_URL=postgresql+psycopg2://user:password@host:port/database

# Alertas (Opcional)
ALERT_SLACK_WEBHOOK=https://hooks.slack.com/services/XXX
ALERT_TELEGRAM_BOT=123456:ABCDEF
ALERT_TELEGRAM_CHAT=-100123456

# SLO Targets
SLO_LATENCY_MS=800
SLO_UPTIME_TARGET=99.5

# Configurações de Monitoramento
MONITOR_CHECK_INTERVAL=60
MAX_LISTENER_LAG_SEC=180
```

### 2. Criar Tabelas no Banco de Dados

As tabelas são criadas automaticamente na primeira execução, mas você pode criá-las manualmente:

```sql
-- Tabela de métricas
CREATE TABLE IF NOT EXISTS monitor_metrics(
    id SERIAL PRIMARY KEY,
    ts TIMESTAMP DEFAULT NOW(),
    check_name TEXT,
    ok BOOLEAN,
    latency_ms INT,
    details JSONB
);

-- Tabela de incidentes
CREATE TABLE IF NOT EXISTS monitor_incidents(
    id SERIAL PRIMARY KEY,
    opened_at TIMESTAMP DEFAULT NOW(),
    resolved_at TIMESTAMP,
    severity TEXT,
    title TEXT,
    detail TEXT
);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_monitor_metrics_ts 
ON monitor_metrics(ts DESC);

CREATE INDEX IF NOT EXISTS idx_monitor_metrics_check_name 
ON monitor_metrics(check_name);
```

---

## 🚀 Executar Monitoramento

### Modo Local

```bash
cd /home/ubuntu/bts-blocktrust/backend
python3 -m monitor.runner
```

### Modo Produção (Render)

Adicione um **Background Worker** no Render:

- **Nome**: `monitor`
- **Comando**: `python3 -m backend.monitor.runner`
- **Instâncias**: 1

---

## 📊 Checks Implementados

### 1. Health Checks da API

| Check | Endpoint | Frequência | SLO |
|-------|----------|-----------|-----|
| `api.health` | `/api/health` | 60s | < 800ms, 99.5% uptime |
| `api.events` | `/api/explorer/events` | 60s | < 800ms, 99.5% uptime |
| `api.contracts` | `/api/explorer/contracts` | 60s | < 800ms |
| `api.stats` | `/api/explorer/stats` | 60s | < 800ms |

### 2. Monitor do Listener

| Check | Descrição | Frequência | Alerta |
|-------|-----------|-----------|--------|
| `listener.lag` | Tempo desde último heartbeat | 60s | > 180s |
| `listener.progress` | Verificar se está processando blocos | 60s | Sem progresso |

### 3. Testes Sintéticos

| Teste | Descrição | Frequência |
|-------|-----------|-----------|
| `synthetic.hash` | Gerar hash de arquivo | 60s |
| `synthetic.wallet_info` | Obter info da carteira | 60s |
| `synthetic.nft_status` | Verificar status do NFT | 60s |

---

## 🚨 Sistema de Alertas

### Níveis de Severidade

- **info** ℹ️: Informativo, sem ação necessária
- **warn** ⚠️: Aviso, requer atenção
- **crit** 🚨: Crítico, requer ação imediata

### Canais de Alerta

#### Slack

Configure o webhook no `.env`:

```bash
ALERT_SLACK_WEBHOOK=https://hooks.slack.com/services/XXX
```

**Exemplo de mensagem**:
```
🚨 [CRIT] API /health indisponível
Status code: 503
```

#### Telegram

Configure o bot e chat ID no `.env`:

```bash
ALERT_TELEGRAM_BOT=123456:ABCDEF
ALERT_TELEGRAM_CHAT=-100123456
```

**Como obter**:
1. Criar bot com [@BotFather](https://t.me/BotFather)
2. Obter token do bot
3. Adicionar bot ao grupo
4. Obter chat ID com [@userinfobot](https://t.me/userinfobot)

---

## 📈 Métricas e SLO

### Service Level Objectives (SLO)

| Métrica | Target | Medição |
|---------|--------|---------|
| **Uptime** | ≥ 99.5% | Últimas 24 horas |
| **Latência P99** | < 800ms | Últimas 24 horas |
| **Listener Lag** | < 180s | Tempo real |

### Consultar Métricas

#### Uptime nas últimas 24 horas

```sql
SELECT 
    check_name,
    COUNT(*) FILTER (WHERE ok = TRUE) * 100.0 / COUNT(*) as uptime_percent
FROM monitor_metrics
WHERE ts > NOW() - INTERVAL '24 hours'
GROUP BY check_name
ORDER BY uptime_percent DESC;
```

#### Latência P99 nas últimas 24 horas

```sql
SELECT 
    check_name,
    PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY latency_ms) as p99_ms
FROM monitor_metrics
WHERE ts > NOW() - INTERVAL '24 hours'
AND ok = TRUE
GROUP BY check_name
ORDER BY p99_ms DESC;
```

#### Eventos de falha nas últimas 24 horas

```sql
SELECT 
    check_name,
    COUNT(*) as failure_count,
    MAX(ts) as last_failure
FROM monitor_metrics
WHERE ts > NOW() - INTERVAL '24 hours'
AND ok = FALSE
GROUP BY check_name
ORDER BY failure_count DESC;
```

---

## 📊 Dashboard de Monitoramento

### Grafana (Recomendado)

Conecte o Grafana ao PostgreSQL e crie painéis com:

1. **Uptime por Check** (Time Series)
2. **Latência P50/P95/P99** (Time Series)
3. **Taxa de Erros** (Stat)
4. **Listener Lag** (Gauge)
5. **Alertas Recentes** (Table)

### Consultas SQL para Grafana

#### Uptime Time Series

```sql
SELECT 
    $__timeGroup(ts, '5m') as time,
    check_name,
    COUNT(*) FILTER (WHERE ok = TRUE) * 100.0 / COUNT(*) as uptime
FROM monitor_metrics
WHERE $__timeFilter(ts)
GROUP BY time, check_name
ORDER BY time;
```

#### Latência Time Series

```sql
SELECT 
    $__timeGroup(ts, '5m') as time,
    check_name,
    PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY latency_ms) as p99
FROM monitor_metrics
WHERE $__timeFilter(ts)
AND ok = TRUE
GROUP BY time, check_name
ORDER BY time;
```

---

## 🔧 Troubleshooting

### Problema: Monitoramento não inicia

**Sintomas**: Erro ao executar `monitor.runner`

**Soluções**:
1. Verificar variável `DATABASE_URL`
2. Verificar conectividade com o banco
3. Verificar se as tabelas foram criadas

```bash
# Testar conexão
python3 -c "import psycopg2; psycopg2.connect('$DATABASE_URL')"
```

### Problema: Alertas não são enviados

**Sintomas**: Checks falham mas não há alertas

**Soluções**:
1. Verificar variáveis `ALERT_SLACK_WEBHOOK` ou `ALERT_TELEGRAM_BOT`
2. Testar webhook manualmente:

```bash
# Slack
curl -X POST $ALERT_SLACK_WEBHOOK \
  -H 'Content-Type: application/json' \
  -d '{"text":"Teste de alerta"}'

# Telegram
curl "https://api.telegram.org/bot$ALERT_TELEGRAM_BOT/sendMessage" \
  -d "chat_id=$ALERT_TELEGRAM_CHAT" \
  -d "text=Teste de alerta"
```

### Problema: Listener sempre marcado como atrasado

**Sintomas**: `listener.lag` sempre falha

**Soluções**:
1. Verificar se o listener está rodando
2. Verificar se o heartbeat está sendo salvo
3. Ajustar `MAX_LISTENER_LAG_SEC` se necessário

```sql
-- Verificar últimos heartbeats
SELECT * FROM monitor_metrics
WHERE check_name = 'listener.tick'
ORDER BY ts DESC
LIMIT 10;
```

---

## 📝 Boas Práticas

### 1. Monitoramento Contínuo

- ✅ Mantenha o monitoramento rodando 24/7
- ✅ Configure alertas para Slack/Telegram
- ✅ Revise métricas semanalmente

### 2. Resposta a Incidentes

- ✅ Defina playbooks para cada tipo de alerta
- ✅ Documente incidentes e resoluções
- ✅ Faça post-mortems após incidentes críticos

### 3. Otimização

- ✅ Ajuste SLOs baseado em dados reais
- ✅ Adicione novos checks conforme necessário
- ✅ Archive métricas antigas (> 30 dias)

### 4. Segurança

- ✅ Não exponha métricas publicamente
- ✅ Use credenciais dedicadas para monitoramento
- ✅ Rotacione tokens de alerta periodicamente

---

## 📚 Referências

- [Prometheus Best Practices](https://prometheus.io/docs/practices/)
- [Google SRE Book](https://sre.google/sre-book/table-of-contents/)
- [Grafana Documentation](https://grafana.com/docs/)

---

## ✅ Checklist de Deploy

- [ ] Variáveis de ambiente configuradas
- [ ] Tabelas de monitoramento criadas
- [ ] Background Worker configurado no Render
- [ ] Alertas testados (Slack/Telegram)
- [ ] Dashboard Grafana configurado (opcional)
- [ ] SLOs definidos e documentados
- [ ] Playbooks de resposta a incidentes criados

---

**Status**: ✅ **Sistema de Monitoramento Pronto para Produção**

*Documentação gerada automaticamente por Manus AI Agent*

