# ⚡ Deploy Cheat Sheet - 30 Segundos

## 🎯 Setup Inicial (Primeira vez)

```bash
# 1. Setup automático
chmod +x setup.sh && ./setup.sh

# 2. Criar repo no GitHub
https://github.com/new

# 3. Conectar e enviar
git remote add origin https://github.com/SEU-USUARIO/whatsapp-qr-connector.git
git add .
git commit -m "🎉 First commit"
git push -u origin main
```

---

## 🚀 Deploy Express (Sempre)

```bash
# Opção 1: Script mágico ✨
./deploy.sh

# Opção 2: Manual (3 linhas)
git add .
git commit -m "🔄 Update"
git push origin main
```

---

## 🐳 Easypanel Setup

1. **Create App** → GitHub
2. **Repository**: whatsapp-qr-connector
3. **Build**: Dockerfile
4. **Port**: 8010
5. **Domain**: seu-dominio.com
6. **Deploy** 🚀

---

## 🧪 Teste Local

```bash
python app.py
# → http://localhost:8010
```

---

## 📋 Checklist Rápido

```
✅ Setup executado
✅ GitHub configurado
✅ Primeiro push feito
✅ App criado no Easypanel
✅ Domínio configurado
✅ SSL ativado
✅ App testado
```

---

## 🆘 SOS Rápido

### Push rejeitado?
```bash
git pull origin main
git push origin main
```

### Porta em uso?
```bash
kill -9 $(lsof -ti:8010)
```

### Build falhou?
```bash
docker build -t test .
# Veja os erros
```

---

## 📞 Docs Completas

- **Setup**: `./setup.sh`
- **Deploy**: `DEPLOY.md`
- **Comandos**: `COMANDOS.md`
- **Exemplos**: `EXAMPLES.md`

---

**Tempo total: < 5 minutos** ⚡

**Boa sorte!** 🚀
