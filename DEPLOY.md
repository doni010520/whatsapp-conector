# 🚀 Deploy GitHub → Easypanel - Guia Completo

## 📋 Pré-requisitos

- ✅ Conta no GitHub
- ✅ VPS com Easypanel instalado
- ✅ Domínio (opcional, mas recomendado)

---

## 🔥 PASSO 1: Preparar o Repositório GitHub

### 1.1 Criar Repositório no GitHub

1. Acesse https://github.com
2. Clique em **"New repository"**
3. Nomeie: `whatsapp-qr-connector` (ou outro nome)
4. Marque como **Público** ou **Privado**
5. **NÃO** inicialize com README (já temos)
6. Clique em **"Create repository"**

### 1.2 Subir os Arquivos

Abra o terminal na pasta do projeto e execute:

```bash
# Inicializar Git
git init

# Adicionar todos os arquivos
git add .

# Fazer primeiro commit
git commit -m "🎉 Initial commit - WhatsApp QR Code Connector"

# Adicionar repositório remoto (substitua com SEU link)
git remote add origin https://github.com/SEU-USUARIO/whatsapp-qr-connector.git

# Enviar para GitHub
git branch -M main
git push -u origin main
```

✅ **Pronto!** Seu código está no GitHub.

---

## 🚀 PASSO 2: Deploy no Easypanel

### 2.1 Acessar Easypanel

1. Acesse seu Easypanel: `https://seu-dominio-easypanel.com`
2. Faça login
3. Clique em **"Create New App"** ou **"+ New Service"**

### 2.2 Configurar o App

#### **Aba: General**
- **Name**: `whatsapp-connector` (ou outro nome)
- **Source**: `GitHub`
- **Repository**: Selecione `whatsapp-qr-connector`
- **Branch**: `main`

#### **Aba: Build**
- **Build Type**: `Dockerfile`
- **Dockerfile Path**: `Dockerfile`
- **Context Path**: `/`

#### **Aba: Environment Variables**
Adicione (se necessário):
```
UAZAPI_BASE_URL=https://benitechlab.uazapi.com
PORT=8010
```

#### **Aba: Domains**
- **Add Domain**: 
  - `whatsapp.seudominio.com` (se tiver domínio)
  - OU use o domínio automático do Easypanel
- **SSL**: Ative (automático com Let's Encrypt)

#### **Aba: Resources**
- **Memory**: 512 MB (mínimo) ou 1 GB (recomendado)
- **CPU**: 0.5 vCPU ou mais

#### **Aba: Ports**
- **Container Port**: `8010`
- **Published Port**: `80` ou `443` (automático)

### 2.3 Deploy

1. Clique em **"Deploy"** ou **"Create & Deploy"**
2. Aguarde o build (~2-5 minutos)
3. ✅ Pronto! Aplicação no ar!

---

## 🌐 PASSO 3: Acessar a Aplicação

### Se configurou domínio:
```
https://whatsapp.seudominio.com
```

### Se usa domínio do Easypanel:
```
https://whatsapp-connector-xxx.easypanel.host
```

---

## 🔄 PASSO 4: Atualizações Futuras

### 4.1 Fazer Alterações

```bash
# Editar arquivos conforme necessário
# Ex: vim app.py

# Adicionar mudanças
git add .

# Commitar
git commit -m "✨ Adiciona nova funcionalidade"

# Enviar para GitHub
git push origin main
```

### 4.2 Deploy Automático

O Easypanel pode fazer **deploy automático** a cada push:

1. No Easypanel, vá em seu app
2. **Settings** → **GitHub Integration**
3. Ative **"Auto Deploy"** ou **"Deploy on Push"**
4. ✅ Agora cada `git push` faz deploy automaticamente!

---

## 🔧 PASSO 5: Configurações Avançadas

### 5.1 Configurar SSL (HTTPS)

No Easypanel:
1. Vá em **Domains**
2. Seu domínio deve ter um ✅ verde (SSL ativo)
3. Se não tiver, clique em **"Enable SSL"**
4. Aguarde ~1 minuto (Let's Encrypt)

### 5.2 Logs e Monitoramento

No Easypanel:
- **Logs**: Veja logs em tempo real
- **Metrics**: CPU, memória, tráfego
- **Health Checks**: Configure verificações automáticas

### 5.3 Backup Automático

1. No Easypanel, vá em **Backups**
2. Configure backup periódico
3. Escolha frequência (diário, semanal)

---

## 📊 Exemplo de Configuração Completa Easypanel

```yaml
# Referência (o Easypanel faz isso automaticamente via UI)
name: whatsapp-connector
source:
  type: github
  repo: SEU-USUARIO/whatsapp-qr-connector
  branch: main
build:
  type: dockerfile
  path: Dockerfile
env:
  - UAZAPI_BASE_URL=https://benitechlab.uazapi.com
  - PORT=8010
domains:
  - whatsapp.seudominio.com
resources:
  memory: 1024
  cpu: 0.5
ports:
  - container: 8010
    published: 80
```

---

## 🐛 Troubleshooting

### Erro: "Build Failed"

**Solução:**
1. Verifique se o `Dockerfile` está correto
2. Confira logs de build no Easypanel
3. Teste localmente: `docker build -t test .`

### Erro: "Container Exited"

**Solução:**
1. Veja logs do container no Easypanel
2. Verifique se a porta 8010 está correta
3. Confirme que o comando no Dockerfile está correto

### App não carrega

**Solução:**
1. Verifique se o domínio está apontado corretamente
2. Aguarde propagação DNS (até 24h)
3. Teste com o domínio temporário do Easypanel primeiro

### SSL não ativa

**Solução:**
1. Verifique se o domínio aponta para IP correto
2. Aguarde alguns minutos
3. Tente reativar SSL manualmente no Easypanel

---

## 🎯 Checklist de Deploy

- [ ] Código no GitHub
- [ ] App criado no Easypanel
- [ ] Dockerfile configurado corretamente
- [ ] Variáveis de ambiente definidas
- [ ] Domínio configurado
- [ ] SSL ativado
- [ ] Deploy bem-sucedido
- [ ] App acessível via browser
- [ ] Testado QR Code e Código de Pareamento
- [ ] Auto-deploy configurado (opcional)

---

## 💡 Dicas Pro

### 1. Use Deploy Branches

```bash
# Branch de produção
git checkout main
git push origin main  # → Deploy automático

# Branch de desenvolvimento
git checkout -b dev
git push origin dev  # → Sem deploy (ou deploy em staging)
```

### 2. Configure Health Check

No Easypanel, adicione:
- **Path**: `/health`
- **Interval**: 30s
- **Timeout**: 5s

### 3. Configure Variáveis por Ambiente

```bash
# Produção
UAZAPI_BASE_URL=https://benitechlab.uazapi.com
DEBUG=False

# Desenvolvimento
UAZAPI_BASE_URL=https://dev.uazapi.com
DEBUG=True
```

### 4. Monitore Recursos

Configure alertas no Easypanel:
- CPU > 80%
- Memória > 90%
- App down > 2 min

---

## 🚀 Comandos Úteis Git

```bash
# Ver status
git status

# Ver histórico
git log --oneline

# Criar branch
git checkout -b nova-feature

# Voltar para main
git checkout main

# Mesclar branch
git merge nova-feature

# Atualizar repositório local
git pull origin main

# Ver branches
git branch -a

# Deletar branch
git branch -d nome-branch
```

---

## 📝 Estrutura Recomendada

```
whatsapp-qr-connector/
│
├── app.py              # Backend
├── index.html          # Frontend
├── requirements.txt    # Dependências
├── Dockerfile          # Deploy
├── docker-compose.yml  # Dev local
│
├── README.md           # Docs principal
├── QUICKSTART.md       # Início rápido
├── DEPLOY.md           # Este arquivo
├── EXAMPLES.md         # Exemplos
│
├── .gitignore          # Arquivos ignorados
└── .github/            # (Opcional) GitHub Actions
    └── workflows/
        └── deploy.yml  # CI/CD automático
```

---

## 🎉 Pronto!

Seu app está no ar! 🚀

**Acesse:** https://seu-dominio.com  
**Teste:** Cole um token UazAPI e conecte!

---

## 📞 Suporte

- **Easypanel Docs**: https://easypanel.io/docs
- **GitHub Docs**: https://docs.github.com
- **Docker Docs**: https://docs.docker.com

---

**Desenvolvido por CLAWDEO** 💜
