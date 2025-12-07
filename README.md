# 📱 WhatsApp QR Code Connector

Aplicação web para conectar instâncias do WhatsApp à **UazAPI** através de QR Code ou Código de Pareamento.

## 🚀 Funcionalidades

- ✅ **Conexão via QR Code**: Escaneie o QR Code no WhatsApp do celular
- ✅ **Conexão via Código de Pareamento**: Digite um código de 8 dígitos no WhatsApp
- ✅ **Monitoramento Automático**: Verifica automaticamente quando a conexão é estabelecida
- ✅ **Interface Intuitiva**: Design moderno e responsivo
- ✅ **Feedback em Tempo Real**: Indicadores visuais de status da conexão

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Conta na UazAPI (https://benitechlab.uazapi.com)
- Token de instância UazAPI

## 🔧 Instalação

### 1. Clone o repositório (ou baixe os arquivos)

```bash
git clone <seu-repositorio>
cd whatsapp-qr-connector
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv
```

### 3. Ative o ambiente virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

## 🏃 Como Usar

### 1. Inicie o servidor

```bash
python app.py
```

Ou com Uvicorn:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8010
```

### 2. Acesse a aplicação

Abra seu navegador e acesse:
```
http://localhost:8010
```

### 3. Conecte seu WhatsApp

#### Opção A: QR Code
1. Selecione "QR Code"
2. Cole o token da sua instância UazAPI
3. Clique em "Conectar WhatsApp"
4. Escaneie o QR Code com o WhatsApp do celular
5. Aguarde a confirmação de conexão

#### Opção B: Código de Pareamento
1. Selecione "Código de Pareamento"
2. Cole o token da sua instância UazAPI
3. Digite o número de WhatsApp (formato: 5511999999999)
4. Clique em "Conectar WhatsApp"
5. Digite o código de 8 dígitos no WhatsApp do celular
6. Aguarde a confirmação de conexão

## 📁 Estrutura do Projeto

```
whatsapp-qr-connector/
│
├── app.py              # Backend FastAPI
├── index.html          # Frontend
├── requirements.txt    # Dependências Python
└── README.md          # Este arquivo
```

## 🔌 Endpoints da API

### POST `/api/connect`
Inicia o processo de conexão

**Request Body:**
```json
{
  "instance_token": "seu-token-aqui",
  "phone": "5511999999999"  // Opcional
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "qrCode": "data:image/png;base64,...",  // Se sem phone
    "pairingCode": "ABCD1234"                // Se com phone
  },
  "message": "Conexão iniciada com sucesso",
  "session_id": "seu-token-aqui"
}
```

### POST `/api/status`
Verifica o status da conexão

**Request Body:**
```json
{
  "instance_token": "seu-token-aqui"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "connected",  // disconnected, connecting, connected
    "phone": "5511999999999"
  }
}
```

### GET `/health`
Health check do servidor

**Response:**
```json
{
  "status": "healthy",
  "active_sessions": 2,
  "timestamp": "2024-12-04T10:30:00"
}
```

## 🎨 Personalização

### Cores e Tema

Edite o arquivo `index.html` na seção `<style>` para personalizar:

```css
/* Gradiente de fundo */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Cor do WhatsApp */
background: #25D366;

/* Cores dos botões */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Logo e Ícones

Substitua o emoji 📱 por uma imagem:

```html
<div class="whatsapp-icon">
    <img src="seu-logo.png" alt="Logo">
</div>
```

## 🚀 Deploy em Produção

### Opção 1: VPS (Ubuntu)

```bash
# Instalar dependências
sudo apt update
sudo apt install python3-pip python3-venv nginx

# Clonar projeto
git clone <seu-repositorio>
cd whatsapp-qr-connector

# Configurar ambiente
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Instalar Gunicorn
pip install gunicorn

# Rodar aplicação
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8010
```

### Opção 2: Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8010

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8010"]
```

Build e run:
```bash
docker build -t whatsapp-connector .
docker run -p 8010:8010 whatsapp-connector
```

### Opção 3: Plataformas Cloud

#### Railway
1. Crie conta no Railway
2. Conecte seu repositório GitHub
3. Configure o build: `pip install -r requirements.txt`
4. Configure o start: `uvicorn app:app --host 0.0.0.0 --port $PORT`

#### Render
1. Crie conta no Render
2. Novo Web Service
3. Conecte repositório
4. Build: `pip install -r requirements.txt`
5. Start: `uvicorn app:app --host 0.0.0.0 --port $PORT`

#### Fly.io
```bash
flyctl launch
flyctl deploy
```

## 🔒 Segurança

### Recomendações para Produção:

1. **Adicione autenticação**: Implemente login de usuários
2. **Use HTTPS**: Configure SSL/TLS (Let's Encrypt)
3. **Rate Limiting**: Limite requisições por IP
4. **Validação de entrada**: Valide todos os dados recebidos
5. **Logs**: Implemente sistema de logging
6. **Armazenamento persistente**: Use Redis ou banco de dados ao invés de memória

### Exemplo de Rate Limiting:

```python
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

@app.post("/api/connect", dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def connect_whatsapp(request: ConnectRequest):
    # ...
```

## 🐛 Troubleshooting

### Erro: "Port already in use"
```bash
# Matar processo na porta 8010
lsof -ti:8010 | xargs kill -9
```

### Erro: "Module not found"
```bash
# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

### QR Code não aparece
- Verifique se o token da instância está correto
- Verifique se a instância está ativa na UazAPI
- Verifique os logs do servidor para erros

### Conexão não detectada automaticamente
- O monitoramento verifica a cada 3 segundos
- Você pode clicar manualmente em "Verificar Status"
- Verifique se a instância está realmente conectada na UazAPI

## 📝 Variáveis de Ambiente

Crie um arquivo `.env` (opcional):

```env
UAZAPI_BASE_URL=https://benitechlab.uazapi.com
PORT=8010
DEBUG=False
```

Use com python-dotenv:
```python
from dotenv import load_dotenv
load_dotenv()
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é open source e está disponível sob a licença MIT.

## 📞 Suporte

- 📧 Email: [seu-email]
- 💬 WhatsApp: [seu-whatsapp]
- 🐛 Issues: [github-issues]

## 🎯 Roadmap

- [ ] Autenticação de usuários
- [ ] Dashboard de instâncias conectadas
- [ ] Histórico de conexões
- [ ] Notificações por email/webhook
- [ ] API para integração com outros sistemas
- [ ] Suporte a múltiplas instâncias simultâneas
- [ ] Reconnect automático em caso de desconexão

## 🙏 Agradecimentos

- UazAPI pela API de WhatsApp Business
- FastAPI pela framework incrível
- Comunidade Python

---

Desenvolvido com ❤️ por CLAWDEO
