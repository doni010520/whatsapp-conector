from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Optional, Dict
import httpx
import asyncio
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

# Base URL da UazAPI
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
    """Iniciar conexão do WhatsApp via QR Code ou Código de Pareamento"""
    
    logger.info(f"Iniciando conexão para instância: {request.instance_token[:8]}...")
    
    try:
        # Validar formato do token
        if len(request.instance_token) < 10:
            raise HTTPException(
                status_code=400,
                detail="Token da instância inválido"
            )
        
        # Preparar headers
        headers = {
            "Content-Type": "application/json"
        }
        
        # URL base da instância
        instance_url = f"{UAZAPI_BASE_URL}/instance/{request.instance_token}"
        
        # Configurar timeout
        timeout = httpx.Timeout(30.0, connect=10.0)
        
        async with httpx.AsyncClient(timeout=timeout) as client:
            # Verificar se a instância existe
            try:
                check_response = await client.get(
                    f"{instance_url}/status",
                    headers=headers
                )
                
                if check_response.status_code == 404:
                    logger.error(f"Instância não encontrada: {request.instance_token[:8]}...")
                    return JSONResponse(
                        status_code=400,
                        content={
                            "success": False,
                            "message": "Instância não encontrada. Verifique o token.",
                            "error": "instance_not_found"
                        }
                    )
                    
            except httpx.ConnectError:
                logger.error("Erro ao conectar com a API UazAPI")
                return JSONResponse(
                    status_code=503,
                    content={
                        "success": False,
                        "message": "Não foi possível conectar com o servidor UazAPI",
                        "error": "connection_error"
                    }
                )
            
            # Decidir se usa QR Code ou Código de Pareamento
            if request.phone:
                # Validar formato do telefone
                phone = request.phone.strip().replace("+", "").replace(" ", "").replace("-", "")
                
                if not phone.isdigit() or len(phone) < 10:
                    return JSONResponse(
                        status_code=400,
                        content={
                            "success": False,
                            "message": "Número de telefone inválido. Use o formato: 5511999999999",
                            "error": "invalid_phone"
                        }
                    )
                
                logger.info(f"Solicitando código de pareamento para: {phone}")
                
                # Solicitar código de pareamento
                try:
                    pairing_response = await client.post(
                        f"{instance_url}/qr/pairing-code",
                        json={"phone": phone},
                        headers=headers
                    )
                    
                    if pairing_response.status_code != 200:
                        error_detail = pairing_response.text
                        logger.error(f"Erro ao gerar código: {error_detail}")
                        return JSONResponse(
                            status_code=pairing_response.status_code,
                            content={
                                "success": False,
                                "message": "Erro ao gerar código de pareamento",
                                "error": "pairing_code_error",
                                "details": error_detail
                            }
                        )
                    
                    pairing_data = pairing_response.json()
                    
                    # Armazenar sessão
                    active_sessions[request.instance_token] = {
                        "phone": phone,
                        "type": "pairing",
                        "created_at": datetime.now().isoformat()
                    }
                    
                    return {
                        "success": True,
                        "data": {
                            "pairingCode": pairing_data.get("pairingCode", ""),
                            "phone": phone
                        },
                        "message": "Código de pareamento gerado com sucesso",
                        "session_id": request.instance_token
                    }
                    
                except httpx.TimeoutException:
                    logger.error("Timeout ao gerar código de pareamento")
                    return JSONResponse(
                        status_code=504,
                        content={
                            "success": False,
                            "message": "Tempo esgotado ao gerar código de pareamento",
                            "error": "timeout"
                        }
                    )
                    
            else:
                # Solicitar QR Code
                logger.info("Solicitando QR Code")
                
                try:
                    qr_response = await client.get(
                        f"{instance_url}/qr/image",
                        headers=headers
                    )
                    
                    if qr_response.status_code != 200:
                        error_detail = qr_response.text
                        logger.error(f"Erro ao gerar QR Code: {error_detail}")
                        return JSONResponse(
                            status_code=qr_response.status_code,
                            content={
                                "success": False,
                                "message": "Erro ao gerar QR Code",
                                "error": "qr_code_error",
                                "details": error_detail
                            }
                        )
                    
                    qr_data = qr_response.json()
                    
                    # Armazenar sessão
                    active_sessions[request.instance_token] = {
                        "type": "qr",
                        "created_at": datetime.now().isoformat()
                    }
                    
                    return {
                        "success": True,
                        "data": {
                            "qrCode": qr_data.get("qrCode", "")
                        },
                        "message": "QR Code gerado com sucesso",
                        "session_id": request.instance_token
                    }
                    
                except httpx.TimeoutException:
                    logger.error("Timeout ao gerar QR Code")
                    return JSONResponse(
                        status_code=504,
                        content={
                            "success": False,
                            "message": "Tempo esgotado ao gerar QR Code",
                            "error": "timeout"
                        }
                    )
                    
    except HTTPException as he:
        raise he
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
    """Verificar o status da conexão"""
    
    logger.info(f"Verificando status para: {request.instance_token[:8]}...")
    
    try:
        headers = {
            "Content-Type": "application/json"
        }
        
        instance_url = f"{UAZAPI_BASE_URL}/instance/{request.instance_token}"
        
        timeout = httpx.Timeout(15.0, connect=5.0)
        
        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                status_response = await client.get(
                    f"{instance_url}/status",
                    headers=headers
                )
                
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    
                    return {
                        "success": True,
                        "data": {
                            "status": status_data.get("status", "unknown"),
                            "phone": status_data.get("phone", "")
                        }
                    }
                else:
                    return JSONResponse(
                        status_code=status_response.status_code,
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
