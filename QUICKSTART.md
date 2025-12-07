# 🚀 Guia de Início Rápido - WhatsApp QR Code Connector

## ⚡ Instalação Express (5 minutos)

### 1️⃣ Baixe e prepare o ambiente

```bash
# Baixe os arquivos
cd whatsapp-qr-connector

# Crie ambiente virtual
python -m venv venv

# Ative (Windows)
venv\Scripts\activate

# Ative (Linux/Mac)
source venv/bin/activate

# Instale dependências
pip install -r requirements.txt
```

### 2️⃣ Inicie o servidor

```bash
python app.py
```

✅ Servidor rodando em: http://localhost:8010

### 3️⃣ Conecte seu WhatsApp

1. Abra http://localhost:8010 no navegador
2. Cole seu token da UazAPI
3. Escolha QR Code ou Código de Pareamento
4. Siga as instruções na tela
5. Pronto! 🎉

---

## 🐳 Com Docker (ainda mais fácil)

```bash
# Build e execute
docker-compose up --build

# Ou apenas execute (se já buildou antes)
docker-compose up
```

Acesse: http://localhost:8010

---

## 🧪 Testar a API

```bash
# Edite test_api.py e adicione seu token
python test_api.py
```

---

## 📱 Onde conseguir o Token da Instância?

1. Acesse: https://benitechlab.uazapi.com
2. Crie uma conta (se não tiver)
3. Crie uma nova instância
4. Copie o token gerado
5. Use na aplicação

---

## 🆘 Problemas Comuns

### Porta 8010 já em uso?
```bash
# Use outra porta
uvicorn app:app --port 8001
```

### Dependências não instalam?
```bash
# Atualize o pip
pip install --upgrade pip

# Tente novamente
pip install -r requirements.txt
```

### QR Code não aparece?
- ✅ Verifique se o token está correto
- ✅ Verifique se a instância está ativa na UazAPI
- ✅ Olhe os logs do terminal para erros

---

## 📞 Suporte Rápido

Erro específico? Envie:
1. Mensagem de erro completa
2. Versão do Python (`python --version`)
3. Sistema operacional

---

## 🎯 Próximos Passos

Depois de conectar:
- [ ] Personalize o design em `index.html`
- [ ] Configure domínio próprio
- [ ] Adicione SSL/HTTPS
- [ ] Integre com seu sistema

---

**Tempo total: ~5 minutos** ⚡

Desenvolvido por CLAWDEO 🚀
