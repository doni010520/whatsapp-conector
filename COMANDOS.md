# 🎯 Guia Rápido de Comandos - Deploy

## 📦 Setup Inicial (Uma única vez)

```bash
# 1. Inicializar Git
git init

# 2. Adicionar repositório remoto
git remote add origin https://github.com/SEU-USUARIO/whatsapp-qr-connector.git

# 3. Primeiro commit
git add .
git commit -m "🎉 Initial commit"
git branch -M main
git push -u origin main
```

---

## 🚀 Deploy Rápido (Use sempre)

### Opção 1: Script Automático (RECOMENDADO)
```bash
# Torna executável (apenas primeira vez)
chmod +x deploy.sh

# Executa deploy
./deploy.sh
```

### Opção 2: Manual (3 comandos)
```bash
git add .
git commit -m "🔄 Sua mensagem aqui"
git push origin main
```

---

## 🔄 Comandos Git Essenciais

### Ver status
```bash
git status
```

### Ver histórico
```bash
git log --oneline --graph
```

### Desfazer mudanças (CUIDADO!)
```bash
# Desfazer mudanças não commitadas
git checkout -- arquivo.py

# Desfazer último commit (mantém alterações)
git reset --soft HEAD~1

# Desfazer último commit (descarta alterações)
git reset --hard HEAD~1
```

### Criar branch
```bash
git checkout -b nova-feature
```

### Trocar de branch
```bash
git checkout main
```

### Mesclar branch
```bash
git checkout main
git merge nova-feature
```

### Atualizar do GitHub
```bash
git pull origin main
```

---

## 🐳 Docker Local

### Build
```bash
docker build -t whatsapp-connector .
```

### Run
```bash
docker run -p 8010:8010 whatsapp-connector
```

### Docker Compose
```bash
# Iniciar
docker-compose up

# Iniciar em background
docker-compose up -d

# Parar
docker-compose down

# Rebuild
docker-compose up --build
```

---

## 🛠️ Easypanel

### Via Interface
1. Acesse Easypanel
2. Apps → Create New App
3. GitHub → Selecione repositório
4. Configure variáveis
5. Deploy

### Logs
```
Easypanel → Seu App → Logs
```

### Restart
```
Easypanel → Seu App → Actions → Restart
```

### Rebuild
```
Easypanel → Seu App → Actions → Rebuild
```

---

## 📊 Verificações Rápidas

### Testar localmente
```bash
python app.py
# Acesse: http://localhost:8010
```

### Testar API
```bash
python test_api.py
```

### Ver logs em produção
```bash
# No Easypanel → Logs
# Ou via SSH na VPS:
docker logs nome-do-container
```

---

## 🆘 Solução Rápida de Problemas

### Git: "nothing to commit"
```bash
# Verifique se fez alterações
git status

# Se não há mudanças, está tudo atualizado!
```

### Git: "Push rejected"
```bash
# Baixe mudanças do GitHub primeiro
git pull origin main

# Depois faça push
git push origin main
```

### Docker: "Port already in use"
```bash
# Encontre processo na porta 8010
lsof -ti:8010

# Mate processo
kill -9 $(lsof -ti:8010)
```

### Easypanel: "Build Failed"
```bash
# 1. Verifique Dockerfile
# 2. Teste build local: docker build -t test .
# 3. Veja logs de build no Easypanel
```

---

## 📋 Checklist de Deploy

```
┌─────────────────────────────────────┐
│ ✅ Código testado localmente       │
│ ✅ Arquivo .env configurado         │
│ ✅ Mudanças commitadas              │
│ ✅ Push para GitHub                 │
│ ✅ Easypanel atualizado             │
│ ✅ App rodando                      │
│ ✅ SSL ativado                      │
│ ✅ Testado em produção              │
└─────────────────────────────────────┘
```

---

## 🎯 Workflow Ideal

```
┌──────────────┐
│ 1. Desenvolver│
│   localmente  │
└───────┬───────┘
        │
┌───────▼────────┐
│ 2. Testar com  │
│  python app.py │
└───────┬────────┘
        │
┌───────▼────────┐
│ 3. Commitar    │
│   git commit   │
└───────┬────────┘
        │
┌───────▼────────┐
│ 4. Push GitHub │
│    git push    │
└───────┬────────┘
        │
┌───────▼────────┐
│ 5. Easypanel   │
│  auto-deploy   │
└───────┬────────┘
        │
┌───────▼────────┐
│ 6. ✅ Online!  │
└────────────────┘
```

---

## 🔥 Comandos Ninja

### Commit rápido
```bash
git add . && git commit -m "🔄 Update" && git push
```

### Ver tamanho do repositório
```bash
git count-objects -vH
```

### Limpar histórico (CUIDADO!)
```bash
git gc --aggressive --prune=now
```

### Ver quem modificou um arquivo
```bash
git blame arquivo.py
```

### Buscar no histórico
```bash
git log --all --grep="mensagem"
```

---

## 💡 Dicas Pro

1. **Commits frequentes**: Faça commits pequenos e frequentes
2. **Mensagens descritivas**: Use emojis e seja claro
3. **Branches**: Use branches para features grandes
4. **Teste antes**: Sempre teste localmente antes de push
5. **Auto-deploy**: Configure no Easypanel para facilitar

---

## 📞 Links Úteis

- **Git Cheat Sheet**: https://training.github.com/downloads/github-git-cheat-sheet/
- **Docker Docs**: https://docs.docker.com
- **Easypanel Docs**: https://easypanel.io/docs

---

**💪 Você consegue! Deploy com confiança!** 🚀
