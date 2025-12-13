from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict
import httpx
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="WhatsApp QR Connector")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base URL da UazAPI (conforme documentação)
UAZAPI_BASE_URL = "https://benitechlab.uazapi.com"

# Armazenar sessões ativas (em produção, use Redis ou banco de dados)
active_sessions: Dict[str, dict] = {}

class ConnectRequest(BaseModel):
    instance_token: str = Field(..., min_length=1, description="Token da instância UazAPI")
    phone: Optional[str] = Field(None, description="Número do WhatsApp para código de pareamento")

class StatusRequest(BaseModel):
    instance_token: str = Field(..., min_length=1)

@app.get("/", response_class=HTMLResponse)
async def root():
    """Servir a página HTML principal"""
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(
            content="<h1>Erro: index.html não encontrado</h1>",
            status_code=404
        )

@app.get("/health")
async def health_check():
    """Health check do servidor"""
    return {
        "status": "healthy",
        "active_sessions": len(active_sessions),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/connect")
async def connect_whatsapp(request: ConnectRequest):
    """
    Iniciar conexão do WhatsApp via QR Code ou Código de Pareamento
    
    Conforme documentação UazAPI:
    - Endpoint: POST /instance/connect
    - Header: token: {instance_token}
    - Body: {"phone": "5511999999999"} (opcional)
    - Com phone: gera código de pareamento
    - Sem phone: gera QR Code
    """
    
    logger.info(f"Iniciando conexão para instância: {request.instance_token[:8]}...")
    
    try:
        # Validar formato do token
        if len(request.instance_token) < 10:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "message": "Token da instância inválido",
                    "error": "invalid_token"
                }
            )
        
        # Preparar headers conforme documentação
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "token": request.instance_token  # Token vai no header!
        }
        
        # Preparar body
        body = {}
        if request.phone:
            # Validar e formatar telefone
            phone = request.phone.strip().replace("+", "").replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
            
            if not phone.isdigit() or len(phone) < 10:
                return JSONResponse(
                    status_code=400,
                    content={
                        "success": False,
                        "message": "Número de telefone inválido. Use o formato: 5511999999999",
                        "error": "invalid_phone"
                    }
                )
            
            body["phone"] = phone
            logger.info(f"Solicitando código de pareamento para: {phone}")
        else:
            logger.info("Solicitando QR Code")
        
        # Configurar timeout
        timeout = httpx.Timeout(30.0, connect=10.0)
        
        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                # Fazer requisição ao endpoint correto
                response = await client.post(
                    f"{UAZAPI_BASE_URL}/instance/connect",
                    headers=headers,
                    json=body if body else None
                )
                
                logger.info(f"Status da resposta: {response.status_code}")
                
                # Tratar diferentes status codes conforme documentação
                if response.status_code == 200:
                    # Sucesso
                    data = response.json()
                    
                    # Armazenar sessão
                    active_sessions[request.instance_token] = {
                        "phone": body.get("phone", ""),
                        "type": "pairing" if body.get("phone") else "qr",
                        "created_at": datetime.now().isoformat()
                    }
                    
                    logger.info(f"Conexão iniciada com sucesso. Tipo: {'pareamento' if body.get('phone') else 'QR Code'}")
                    
                    return {
                        "success": True,
                        "data": data,
                        "message": "Conexão iniciada com sucesso",
                        "session_id": request.instance_token
                    }
                
                elif response.status_code == 401:
                    # Token inválido/expirado
                    logger.error("Token inválido ou expirado")
                    return JSONResponse(
                        status_code=401,
                        content={
                            "success": False,
                            "message": "Token inválido ou expirado",
                            "error": "invalid_token"
                        }
                    )
                
                elif response.status_code == 404:
                    # Instância não encontrada
                    logger.error("Instância não encontrada")
                    return JSONResponse(
                        status_code=404,
                        content={
                            "success": False,
                            "message": "Instância não encontrada. Verifique se o token está correto.",
                            "error": "instance_not_found"
                        }
                    )
                
                elif response.status_code == 429:
                    # Limite de conexões simultâneas atingido
                    logger.error("Limite de conexões simultâneas atingido")
                    return JSONResponse(
                        status_code=429,
                        content={
                            "success": False,
                            "message": "Limite de conexões simultâneas atingido. Tente novamente em alguns instantes.",
                            "error": "rate_limit"
                        }
                    )
                
                elif response.status_code == 500:
                    # Erro interno da UazAPI
                    logger.error("Erro interno da UazAPI")
                    error_detail = response.text
                    return JSONResponse(
                        status_code=500,
                        content={
                            "success": False,
                            "message": "Erro interno do servidor UazAPI",
                            "error": "uazapi_error",
                            "details": error_detail
                        }
                    )
                
                else:
                    # Status code não documentado
                    logger.error(f"Status code inesperado: {response.status_code}")
                    return JSONResponse(
                        status_code=response.status_code,
                        content={
                            "success": False,
                            "message": f"Erro ao conectar. Status: {response.status_code}",
                            "error": "unexpected_error",
                            "details": response.text
                        }
                    )
                    
            except httpx.TimeoutException:
                logger.error("Timeout ao conectar com UazAPI")
                return JSONResponse(
                    status_code=504,
                    content={
                        "success": False,
                        "message": "Tempo esgotado ao conectar. Tente novamente.",
                        "error": "timeout"
                    }
                )
            
            except httpx.ConnectError as e:
                logger.error(f"Erro de conexão com UazAPI: {str(e)}")
                return JSONResponse(
                    status_code=503,
                    content={
                        "success": False,
                        "message": "Não foi possível conectar com o servidor UazAPI",
                        "error": "connection_error"
                    }
                )
                    
    except Exception as e:
        logger.error(f"Erro inesperado ao conectar: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Erro interno do servidor",
                "error": "internal_error",
                "details": str(e)
            }
        )

@app.post("/api/status")
async def check_status(request: StatusRequest):
    """
    Verificar o status da conexão
    
    Conforme documentação UazAPI:
    - Endpoint: GET /instance/status
    - Header: token: {instance_token}
    - Estados: disconnected, connecting, connected
    """
    
    logger.info(f"Verificando status para: {request.instance_token[:8]}...")
    
    try:
        # Preparar headers
        headers = {
            "Accept": "application/json",
            "token": request.instance_token
        }
        
        timeout = httpx.Timeout(15.0, connect=5.0)
        
        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                response = await client.get(
                    f"{UAZAPI_BASE_URL}/instance/status",
                    headers=headers
                )
                
                logger.info(f"Status code: {response.status_code}")
                
                if response.status_code == 200:
                    status_data = response.json()
                    
                    logger.info(f"Status obtido: {status_data.get('status', 'unknown')}")
                    
                    return {
                        "success": True,
                        "data": status_data
                    }
                
                elif response.status_code == 401:
                    return JSONResponse(
                        status_code=401,
                        content={
                            "success": False,
                            "message": "Token inválido ou expirado",
                            "error": "invalid_token"
                        }
                    )
                
                elif response.status_code == 404:
                    return JSONResponse(
                        status_code=404,
                        content={
                            "success": False,
                            "message": "Instância não encontrada",
                            "error": "instance_not_found"
                        }
                    )
                
                else:
                    return JSONResponse(
                        status_code=response.status_code,
                        content={
                            "success": False,
                            "message": "Erro ao verificar status",
                            "error": "status_check_error"
                        }
                    )
                    
            except httpx.TimeoutException:
                logger.error("Timeout ao verificar status")
                return JSONResponse(
                    status_code=504,
                    content={
                        "success": False,
                        "message": "Tempo esgotado ao verificar status",
                        "error": "timeout"
                    }
                )
            
            except httpx.ConnectError:
                logger.error("Erro de conexão ao verificar status")
                return JSONResponse(
                    status_code=503,
                    content={
                        "success": False,
                        "message": "Não foi possível conectar com o servidor",
                        "error": "connection_error"
                    }
                )
                
    except Exception as e:
        logger.error(f"Erro inesperado ao verificar status: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Erro interno do servidor",
                "error": "internal_error",
                "details": str(e)
            }
        )

# Tratamento global de erros
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Erro não tratado: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Erro interno do servidor",
            "error": "internal_error"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8010)
