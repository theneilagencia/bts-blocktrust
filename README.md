# 🏛️ BTS Blocktrust

Sistema descentralizado para registro, assinatura e verificação de documentos com blockchain Polygon.

## 🚀 Características

- ✅ Registro seguro de documentos na blockchain
- ✅ Verificação de autenticidade instantânea
- ✅ Privacidade total (apenas hash trafega)
- ✅ KYC integrado com Sumsub
- ✅ Interface moderna e responsiva
- ✅ Conformidade LGPD

## 🛠️ Tecnologias

### Frontend
- React 18 + TypeScript
- Tailwind CSS
- Vite
- Axios
- React Router

### Backend
- Flask (Python)
- PostgreSQL
- JWT Authentication
- SendGrid (emails)

### Blockchain
- Toolblox (Polygon Amoy/Mainnet)
- SHA-256 hashing

## 📦 Instalação Local

### Pré-requisitos
- Node.js 22+
- Python 3.11+
- PostgreSQL

### 1. Clone o repositório
```bash
git clone https://github.com/theneilagencia/bts-blocktrust.git
cd bts-blocktrust
```

### 2. Configure as variáveis de ambiente
```bash
cp .env.example .env
# Edite .env com suas credenciais
```

### 3. Instale as dependências

**Backend:**
```bash
cd api
pip install -r requirements.txt
```

**Frontend:**
```bash
pnpm install
```

### 4. Inicie o desenvolvimento

**Backend:**
```bash
cd api
python app.py
```

**Frontend:**
```bash
pnpm dev
```

Acesse: http://localhost:5173

## 🌐 Deploy no Render

### 1. Conecte o repositório ao Render
- Acesse https://render.com
- Conecte sua conta GitHub
- Selecione o repositório `bts-blocktrust`

### 2. Configure as variáveis de ambiente no Render
```
DATABASE_URL=<sua-database-url>
JWT_SECRET=<seu-jwt-secret>
SENDGRID_API_KEY=<sua-sendgrid-key>
TOOLBLOX_MINT_IDENTITY_URL=<toolblox-url-identity>
TOOLBLOX_REGISTER_SIGNATURE_URL=<toolblox-url-signature>
TOOLBLOX_VERIFY_URL=<toolblox-url-verify>
SUMSUB_APP_TOKEN=<sumsub-token>
SUMSUB_SECRET_KEY=<sumsub-secret>
```

### 3. Deploy automático
O Render detectará o `render.yaml` e fará o deploy automaticamente.

## 📚 Estrutura do Projeto

```
bts-blocktrust/
├── api/                    # Backend Flask
│   ├── routes/            # Rotas da API
│   ├── utils/             # Utilitários (DB, mail, etc.)
│   ├── app.py             # Aplicação principal
│   └── requirements.txt   # Dependências Python
├── src/                   # Frontend React
│   ├── app/              # Páginas
│   ├── components/       # Componentes UI
│   ├── lib/              # Bibliotecas (API, auth, hash)
│   └── main.tsx          # Entry point
├── docs/                 # Documentação
├── tests/                # Testes E2E
├── render.yaml           # Configuração Render
└── README.md
```

## 🔐 Segurança

- Apenas o hash SHA-256 dos documentos é armazenado
- Autenticação JWT com expiração
- Senhas com bcrypt
- Variáveis sensíveis apenas no backend
- Conformidade LGPD

## 📄 Licença

© 2024 BTS Blocktrust. Todos os direitos reservados.

## 📞 Suporte

Email: help@btsglobalcorp.com

