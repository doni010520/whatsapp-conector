# 🔌 Configuração de Portas - WhatsApp QR Code Connector

## 🎯 Porta Configurada

O sistema está configurado para usar a **porta 8010** por padrão.

---

## 📋 Configuração Atual

### **Porta Principal: 8010**

```
✅ Porta padrão: 8010
✅ Configurável via variável de ambiente
✅ Host: 0.0.0.0 (aceita todas as conexões)
```

---

## 🔍 Onde a Porta está Configurada

### 1. **app.py** (Backend)
```python
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8010))  # Padrão: 8010
    uvicorn.run(app, host="0.0.0.0", port=port)
```
✅ **Lê da variável de ambiente PORT, senão usa 8010**

### 2. **.env** (Configuração)
```bash
PORT=8010
```

### 3. **docker-compose.yml** (Docker)
```yaml
ports:
  - "8010:8010"  # host:container
environment:
  - PORT=8010
```
- **8010:8010** = Porta 8010 do host → Porta 8010 do container

### 4. **Dockerfile**
```dockerfile
EXPOSE 8010
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8010"]
```

---

## 🔄 Como Mudar a Porta

### **Opção 1: Arquivo .env (Recomendado)**
```bash
# Edite .env
PORT=3000  # ou qualquer outra porta
```

### **Opção 2: Variável de Ambiente**
```bash
# Linux/Mac
export PORT=3000
python app.py

# Windows (CMD)
set PORT=3000
python app.py

# Windows (PowerShell)
$env:PORT=3000
python app.py
```

### **Opção 3: Docker Compose**
```yaml
# Edite docker-compose.yml
ports:
  - "3000:8010"  # Porta 3000 no host → 8010 no container
environment:
  - PORT=8010    # Porta interna do container
```

### **Opção 4: Comando Direto**
```bash
# Uvicorn diretamente
uvicorn app:app --host 0.0.0.0 --port 3000

# Ou edite app.py e mude o padrão
port = int(os.getenv("PORT", 3000))  # Novo padrão: 3000
```

---

## 🌐 Acesso à Aplicação

### **Desenvolvimento Local**
```
http://localhost:8010
http://127.0.0.1:8010
http://SEU-IP-LOCAL:8010
```

### **Rede Local (outros dispositivos)**
```
http://192.168.x.x:8010
http://10.0.x.x:8010
```

### **Produção (com domínio)**
```
https://seu-dominio.com
https://whatsapp.seu-dominio.com
```
*Nota: Easypanel gerencia automaticamente as portas e SSL*

---

## 🐳 Portas no Docker

### **Mapeamento Padrão**
```yaml
ports:
  - "8010:8010"
```
- **Primeira 8010**: Porta no HOST (seu computador)
- **Segunda 8010**: Porta no CONTAINER (Docker)

### **Exemplos de Mapeamento Alternativo**

**Porta externa diferente:**
```yaml
ports:
  - "3000:8010"  # Acesse em http://localhost:3000
```

**Múltiplas instâncias:**
```yaml
# Instância 1
ports:
  - "8001:8010"

# Instância 2
ports:
  - "8002:8010"

# Instância 3
ports:
  - "8003:8010"
```

---

## 🚀 Easypanel - Configuração de Portas

No Easypanel, configure:

### **1. Container Port (Porta Interna)**
```
Container Port: 8010
```
*Esta é a porta que o app usa internamente*

### **2. Published Port (Porta Externa)**
```
Published Port: 80 (HTTP) ou 443 (HTTPS)
```
*Easypanel gerencia automaticamente*

### **3. Variável de Ambiente**
```
PORT=8010
```

### **Resultado**
- Internamente o app roda na porta 8010
- Externamente acessível via:
  - `http://seu-dominio.com` (porta 80)
  - `https://seu-dominio.com` (porta 443 com SSL)

---

## 🔒 Portas e Firewall

### **Desenvolvimento Local**
```bash
# Liberar porta 8010 (se necessário)

# Linux (UFW)
sudo ufw allow 8010

# Linux (iptables)
sudo iptables -A INPUT -p tcp --dport 8010 -j ACCEPT

# Windows Firewall
# Painel de Controle → Firewall → Regras de Entrada
```

### **Produção (VPS)**
```bash
# Geralmente só precisa liberar 80 e 443
sudo ufw allow 80
sudo ufw allow 443

# Porta 8010 só se acessar direto (não recomendado)
# sudo ufw allow 8010
```

---

## 📊 Resumo das Portas

| Ambiente | Porta | Acesso | SSL |
|----------|-------|--------|-----|
| **Local** | 8010 | http://localhost:8010 | ❌ |
| **Docker Local** | 8010 | http://localhost:8010 | ❌ |
| **VPS (direto)** | 8010 | http://IP:8010 | ❌ |
| **Easypanel** | 80/443 | https://dominio.com | ✅ |

---

## 🧪 Testar Porta

### **Verificar se porta está em uso**
```bash
# Linux/Mac
lsof -i :8010

# Windows
netstat -ano | findstr :8010
```

### **Testar conexão**
```bash
# cURL
curl http://localhost:8010/health

# Navegador
http://localhost:8010

# Python
python -c "import requests; print(requests.get('http://localhost:8010/health').json())"
```

---

## ⚠️ Problemas Comuns

### **Erro: "Port already in use"**
```bash
# Encontrar processo
lsof -i :8010

# Matar processo
kill -9 PID_DO_PROCESSO

# Ou use outra porta
PORT=8001 python app.py
```

### **Erro: "Permission denied" (porta < 1024)**
```bash
# Portas abaixo de 1024 precisam de sudo
sudo python app.py

# Ou use porta acima de 1024
PORT=8010 python app.py  # Recomendado
```

### **Não consegue acessar de outro dispositivo**
```bash
# Verifique se está usando 0.0.0.0 (não 127.0.0.1)
uvicorn app:app --host 0.0.0.0 --port 8010

# Verifique firewall
sudo ufw status
```

---

## 💡 Melhores Práticas

### **Desenvolvimento**
```bash
# Use porta 8010 (padrão)
PORT=8010
```

### **Staging**
```bash
# Use porta diferente se rodar múltiplas versões
PORT=8001  # dev
PORT=8002  # staging
PORT=8003  # preview
```

### **Produção**
```bash
# Deixe Easypanel/Nginx gerenciar
# Internamente: porta 8010
# Externamente: porta 80/443 (gerenciado automaticamente)
```

---

## 🔧 Configuração Avançada

### **Múltiplas Workers**
```bash
# Uvicorn com 4 workers
uvicorn app:app --host 0.0.0.0 --port 8010 --workers 4
```

### **Gunicorn com Uvicorn Workers**
```bash
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8010
```

### **Nginx Reverse Proxy**
```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8010;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 🎯 Checklist de Portas

```
□ Porta configurada em .env (PORT=8010)
□ app.py lê da variável de ambiente
□ Docker Compose mapeia corretamente (8010:8010)
□ Dockerfile expõe porta 8010
□ Firewall permite porta (se necessário)
□ Easypanel configurado com porta 8010
□ SSL configurado (produção)
□ Teste de conexão funcionando
```

---

## 📞 Resumo Rápido

**Porta atual: 8010**

Para alterar, edite:
1. Arquivo `.env`: `PORT=NOVA_PORTA`
2. Ou variável de ambiente: `export PORT=NOVA_PORTA`

Acesse:
- Local: `http://localhost:8010`
- Produção: `https://seu-dominio.com`

**Simples assim!** 🚀
