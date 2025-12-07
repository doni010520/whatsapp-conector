# 📚 Exemplos de Uso - API WhatsApp Connector

## 🔥 Exemplos Práticos

### 1. Conectar via QR Code (Python)

```python
import requests

url = "http://localhost:8010/api/connect"
payload = {
    "instance_token": "seu-token-aqui"
}

response = requests.post(url, json=payload)
result = response.json()

if result.get("success"):
    qr_code = result["data"]["qrCode"]
    print("QR Code gerado!")
    # Salvar em arquivo
    with open("qrcode.txt", "w") as f:
        f.write(qr_code)
else:
    print("Erro:", result.get("detail"))
```

### 2. Conectar via Código de Pareamento (Python)

```python
import requests

url = "http://localhost:8010/api/connect"
payload = {
    "instance_token": "seu-token-aqui",
    "phone": "5511999999999"
}

response = requests.post(url, json=payload)
result = response.json()

if result.get("success"):
    pairing_code = result["data"]["pairingCode"]
    print(f"Código de Pareamento: {pairing_code}")
else:
    print("Erro:", result.get("detail"))
```

### 3. Verificar Status (Python)

```python
import requests

url = "http://localhost:8010/api/status"
payload = {
    "instance_token": "seu-token-aqui"
}

response = requests.post(url, json=payload)
result = response.json()

if result.get("success"):
    status = result["data"]["status"]
    print(f"Status: {status}")
    # disconnected, connecting, connected
else:
    print("Erro:", result.get("detail"))
```

### 4. Monitorar Conexão Automaticamente (Python)

```python
import requests
import time

def monitor_connection(token, max_attempts=20):
    url = "http://localhost:8010/api/status"
    
    for attempt in range(1, max_attempts + 1):
        print(f"Tentativa {attempt}/{max_attempts}...")
        
        response = requests.post(url, json={"instance_token": token})
        result = response.json()
        
        if result.get("success"):
            status = result["data"]["status"]
            print(f"Status: {status}")
            
            if status == "connected":
                print("✅ Conectado com sucesso!")
                return True
            elif status == "disconnected":
                print("❌ Desconectado")
                return False
        
        time.sleep(3)  # Aguarda 3 segundos
    
    print("⏱️ Timeout")
    return False

# Uso
token = "seu-token-aqui"
monitor_connection(token)
```

---

## 🌐 Exemplos JavaScript (Frontend)

### 5. Conectar via QR Code (JavaScript/Fetch)

```javascript
async function connectQRCode() {
    const token = document.getElementById('token').value;
    
    try {
        const response = await fetch('/api/connect', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                instance_token: token
            })
        });

        const result = await response.json();
        
        if (result.success) {
            // Exibir QR Code
            document.getElementById('qrImage').src = result.data.qrCode;
            console.log('QR Code gerado!');
        } else {
            console.error('Erro:', result.detail);
        }
    } catch (error) {
        console.error('Erro na requisição:', error);
    }
}
```

### 6. Conectar via Código de Pareamento (JavaScript)

```javascript
async function connectPairingCode() {
    const token = document.getElementById('token').value;
    const phone = document.getElementById('phone').value;
    
    try {
        const response = await fetch('/api/connect', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                instance_token: token,
                phone: phone
            })
        });

        const result = await response.json();
        
        if (result.success) {
            // Exibir código
            document.getElementById('pairingCode').textContent = 
                result.data.pairingCode;
            console.log('Código gerado!');
        } else {
            console.error('Erro:', result.detail);
        }
    } catch (error) {
        console.error('Erro na requisição:', error);
    }
}
```

### 7. Verificar Status (JavaScript)

```javascript
async function checkStatus() {
    const token = document.getElementById('token').value;
    
    try {
        const response = await fetch('/api/status', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                instance_token: token
            })
        });

        const result = await response.json();
        
        if (result.success) {
            const status = result.data.status;
            console.log('Status:', status);
            
            // Atualizar UI
            updateStatusIndicator(status);
        }
    } catch (error) {
        console.error('Erro:', error);
    }
}

function updateStatusIndicator(status) {
    const indicator = document.getElementById('statusIndicator');
    indicator.className = `status-indicator ${status}`;
}
```

### 8. Monitoramento Automático (JavaScript)

```javascript
let statusCheckInterval = null;

function startMonitoring(token) {
    // Verificar a cada 3 segundos
    statusCheckInterval = setInterval(async () => {
        const response = await fetch('/api/status', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                instance_token: token
            })
        });

        const result = await response.json();
        
        if (result.success) {
            const status = result.data.status;
            console.log('Status atual:', status);
            
            if (status === 'connected') {
                stopMonitoring();
                alert('✅ WhatsApp conectado com sucesso!');
            }
        }
    }, 3000);
}

function stopMonitoring() {
    if (statusCheckInterval) {
        clearInterval(statusCheckInterval);
        statusCheckInterval = null;
    }
}
```

---

## 🔌 Exemplos cURL

### 9. Conectar via QR Code (cURL)

```bash
curl --request POST \
  --url http://localhost:8010/api/connect \
  --header 'Content-Type: application/json' \
  --data '{
    "instance_token": "seu-token-aqui"
  }'
```

### 10. Conectar via Código de Pareamento (cURL)

```bash
curl --request POST \
  --url http://localhost:8010/api/connect \
  --header 'Content-Type: application/json' \
  --data '{
    "instance_token": "seu-token-aqui",
    "phone": "5511999999999"
  }'
```

### 11. Verificar Status (cURL)

```bash
curl --request POST \
  --url http://localhost:8010/api/status \
  --header 'Content-Type: application/json' \
  --data '{
    "instance_token": "seu-token-aqui"
  }'
```

### 12. Health Check (cURL)

```bash
curl --request GET \
  --url http://localhost:8010/health
```

---

## 🔧 Integração com N8N

### 13. Workflow N8N para Conectar WhatsApp

```json
{
  "nodes": [
    {
      "parameters": {
        "method": "POST",
        "url": "http://localhost:8010/api/connect",
        "options": {},
        "bodyParametersJson": "={\n  \"instance_token\": \"{{$node[\"Set Token\"].json[\"token\"]}}\",\n  \"phone\": \"{{$node[\"Set Phone\"].json[\"phone\"]}}\"\n}"
      },
      "name": "Conectar WhatsApp",
      "type": "n8n-nodes-base.httpRequest",
      "position": [250, 300]
    },
    {
      "parameters": {
        "values": {
          "string": [
            {
              "name": "token",
              "value": "seu-token-aqui"
            },
            {
              "name": "phone",
              "value": "5511999999999"
            }
          ]
        }
      },
      "name": "Set Token",
      "type": "n8n-nodes-base.set",
      "position": [50, 300]
    }
  ]
}
```

### 14. Workflow N8N para Monitorar Status

```json
{
  "nodes": [
    {
      "parameters": {
        "rule": {
          "interval": [
            {
              "field": "seconds",
              "secondsInterval": 3
            }
          ]
        }
      },
      "name": "Verificar a cada 3s",
      "type": "n8n-nodes-base.scheduleTrigger",
      "position": [50, 300]
    },
    {
      "parameters": {
        "method": "POST",
        "url": "http://localhost:8010/api/status",
        "bodyParametersJson": "={\n  \"instance_token\": \"{{$node[\"Set\"].json[\"token\"]}}\"\n}"
      },
      "name": "Verificar Status",
      "type": "n8n-nodes-base.httpRequest",
      "position": [250, 300]
    },
    {
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{$json[\"data\"][\"status\"]}}",
              "value2": "connected"
            }
          ]
        }
      },
      "name": "Se Conectado",
      "type": "n8n-nodes-base.if",
      "position": [450, 300]
    }
  ]
}
```

---

## 💡 Dicas de Integração

### 15. Salvar QR Code como Imagem (Python)

```python
import requests
import base64
from PIL import Image
from io import BytesIO

# Conectar e obter QR Code
response = requests.post(
    "http://localhost:8010/api/connect",
    json={"instance_token": "seu-token"}
)
result = response.json()

if result.get("success"):
    # QR Code vem em formato data:image/png;base64,...
    qr_data = result["data"]["qrCode"]
    
    # Remover prefixo
    base64_data = qr_data.split(",")[1]
    
    # Decodificar e salvar
    image_data = base64.b64decode(base64_data)
    image = Image.open(BytesIO(image_data))
    image.save("qrcode.png")
    print("QR Code salvo como qrcode.png")
```

### 16. Enviar QR Code por Email (Python)

```python
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import base64

# Obter QR Code
response = requests.post(
    "http://localhost:8010/api/connect",
    json={"instance_token": "seu-token"}
)
result = response.json()

if result.get("success"):
    qr_data = result["data"]["qrCode"]
    base64_data = qr_data.split(",")[1]
    image_data = base64.b64decode(base64_data)
    
    # Criar email
    msg = MIMEMultipart()
    msg['From'] = "seu-email@gmail.com"
    msg['To'] = "cliente@email.com"
    msg['Subject'] = "Seu QR Code para conectar WhatsApp"
    
    # Corpo do email
    body = "Escaneie o QR Code anexo para conectar seu WhatsApp."
    msg.attach(MIMEText(body, 'plain'))
    
    # Anexar imagem
    image = MIMEImage(image_data, name="qrcode.png")
    msg.attach(image)
    
    # Enviar
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("seu-email@gmail.com", "sua-senha")
    server.send_message(msg)
    server.quit()
    
    print("Email enviado!")
```

---

## 🚀 Exemplos Avançados

### 17. Sistema Completo de Conexão (Python)

```python
import requests
import time
from datetime import datetime

class WhatsAppConnector:
    def __init__(self, base_url="http://localhost:8010"):
        self.base_url = base_url
        self.session_id = None
    
    def connect_qr(self, token):
        """Conectar via QR Code"""
        response = requests.post(
            f"{self.base_url}/api/connect",
            json={"instance_token": token}
        )
        result = response.json()
        
        if result.get("success"):
            self.session_id = result["session_id"]
            return result["data"]["qrCode"]
        return None
    
    def connect_pairing(self, token, phone):
        """Conectar via código de pareamento"""
        response = requests.post(
            f"{self.base_url}/api/connect",
            json={
                "instance_token": token,
                "phone": phone
            }
        )
        result = response.json()
        
        if result.get("success"):
            self.session_id = result["session_id"]
            return result["data"]["pairingCode"]
        return None
    
    def check_status(self):
        """Verificar status da conexão"""
        if not self.session_id:
            return None
        
        response = requests.post(
            f"{self.base_url}/api/status",
            json={"instance_token": self.session_id}
        )
        result = response.json()
        
        if result.get("success"):
            return result["data"]["status"]
        return None
    
    def wait_for_connection(self, timeout=120):
        """Aguardar até conectar ou timeout"""
        start_time = time.time()
        
        while (time.time() - start_time) < timeout:
            status = self.check_status()
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Status: {status}")
            
            if status == "connected":
                return True
            elif status == "disconnected":
                return False
            
            time.sleep(3)
        
        return False

# Uso
connector = WhatsAppConnector()

# Opção 1: QR Code
qr_code = connector.connect_qr("seu-token")
if qr_code:
    print("QR Code gerado! Escaneie agora.")
    if connector.wait_for_connection():
        print("✅ Conectado!")
    else:
        print("❌ Falha na conexão")

# Opção 2: Código de Pareamento
# pairing_code = connector.connect_pairing("seu-token", "5511999999999")
# if pairing_code:
#     print(f"Código: {pairing_code}")
#     if connector.wait_for_connection():
#         print("✅ Conectado!")
```

---

## 📝 Notas Importantes

- ⏱️ QR Codes expiram em 2 minutos
- ⏱️ Códigos de pareamento expiram em 5 minutos
- 🔄 Recomendado verificar status a cada 3 segundos
- 🔒 Nunca exponha tokens em código público
- 📊 Use rate limiting em produção

---

Desenvolvido por CLAWDEO 🚀
