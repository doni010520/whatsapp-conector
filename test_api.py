"""
Script de teste para a API WhatsApp QR Code Connector
"""
import httpx
import asyncio
import json

BASE_URL = "http://localhost:8010"

# Configuração (substitua com seu token real)
INSTANCE_TOKEN = "SEU_TOKEN_AQUI"
PHONE_NUMBER = "5511999999999"  # Opcional

async def test_health():
    """Testa o endpoint de health check"""
    print("\n🔍 Testando Health Check...")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

async def test_connect_qr():
    """Testa conexão via QR Code"""
    print("\n📱 Testando Conexão via QR Code...")
    async with httpx.AsyncClient() as client:
        payload = {
            "instance_token": INSTANCE_TOKEN
        }
        response = await client.post(
            f"{BASE_URL}/api/connect",
            json=payload
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        
        if result.get('success'):
            print(f"Session ID: {result.get('session_id')}")
            if result.get('data', {}).get('qrCode'):
                print("✅ QR Code gerado com sucesso!")
                print(f"QR Code (primeiros 100 chars): {result['data']['qrCode'][:100]}...")
            return result.get('session_id')
        else:
            print(f"❌ Erro: {result}")
    return None

async def test_connect_pairing():
    """Testa conexão via Código de Pareamento"""
    print("\n🔢 Testando Conexão via Código de Pareamento...")
    async with httpx.AsyncClient() as client:
        payload = {
            "instance_token": INSTANCE_TOKEN,
            "phone": PHONE_NUMBER
        }
        response = await client.post(
            f"{BASE_URL}/api/connect",
            json=payload
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        
        if result.get('success'):
            print(f"Session ID: {result.get('session_id')}")
            if result.get('data', {}).get('pairingCode'):
                print(f"✅ Código de Pareamento: {result['data']['pairingCode']}")
            return result.get('session_id')
        else:
            print(f"❌ Erro: {result}")
    return None

async def test_status(session_id):
    """Testa verificação de status"""
    if not session_id:
        print("\n❌ Nenhuma sessão para verificar status")
        return
    
    print(f"\n📊 Testando Verificação de Status (Session: {session_id[:20]}...)...")
    async with httpx.AsyncClient() as client:
        payload = {
            "instance_token": session_id
        }
        response = await client.post(
            f"{BASE_URL}/api/status",
            json=payload
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        
        if result.get('success'):
            status_data = result.get('data', {})
            print(f"✅ Status: {status_data.get('status')}")
            print(f"Response: {json.dumps(status_data, indent=2)}")
        else:
            print(f"❌ Erro: {result}")

async def monitor_connection(session_id, max_attempts=20):
    """Monitora a conexão até ser estabelecida ou timeout"""
    if not session_id:
        print("\n❌ Nenhuma sessão para monitorar")
        return
    
    print(f"\n⏱️ Monitorando Conexão (máximo {max_attempts} tentativas)...")
    
    async with httpx.AsyncClient() as client:
        for attempt in range(1, max_attempts + 1):
            print(f"\nTentativa {attempt}/{max_attempts}...", end=" ")
            
            try:
                payload = {"instance_token": session_id}
                response = await client.post(
                    f"{BASE_URL}/api/status",
                    json=payload
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get('success'):
                        status = result.get('data', {}).get('status')
                        print(f"Status: {status}")
                        
                        if status == 'connected':
                            print("\n✅ WhatsApp CONECTADO com sucesso!")
                            return True
                        elif status == 'disconnected':
                            print("\n❌ WhatsApp DESCONECTADO")
                            return False
                else:
                    print(f"Erro: {response.status_code}")
            
            except Exception as e:
                print(f"Erro: {e}")
            
            await asyncio.sleep(3)  # Aguarda 3 segundos entre verificações
    
    print("\n⏱️ Timeout: Conexão não estabelecida no tempo esperado")
    return False

async def main():
    """Função principal de testes"""
    print("=" * 60)
    print("🧪 TESTES DA API - WhatsApp QR Code Connector")
    print("=" * 60)
    
    # Verificar configuração
    if INSTANCE_TOKEN == "SEU_TOKEN_AQUI":
        print("\n❌ ERRO: Configure o INSTANCE_TOKEN no arquivo test_api.py")
        return
    
    # 1. Health Check
    if not await test_health():
        print("\n❌ Servidor não está respondendo. Verifique se está rodando.")
        return
    
    print("\n" + "=" * 60)
    print("Escolha o método de teste:")
    print("1. QR Code")
    print("2. Código de Pareamento")
    print("3. Ambos")
    print("=" * 60)
    
    choice = input("\nEscolha uma opção (1-3): ").strip()
    
    session_id = None
    
    if choice == "1":
        session_id = await test_connect_qr()
    elif choice == "2":
        session_id = await test_connect_pairing()
    elif choice == "3":
        print("\n--- Testando QR Code ---")
        await test_connect_qr()
        print("\n--- Testando Código de Pareamento ---")
        session_id = await test_connect_pairing()
    else:
        print("\n❌ Opção inválida")
        return
    
    # Verificar status uma vez
    if session_id:
        await test_status(session_id)
        
        # Perguntar se quer monitorar
        monitor = input("\n🔄 Deseja monitorar a conexão automaticamente? (s/n): ").strip().lower()
        if monitor == 's':
            await monitor_connection(session_id)
    
    print("\n" + "=" * 60)
    print("✅ Testes concluídos!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
