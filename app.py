# app.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict
import httpx
from datetime import datetime
import logging
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="WhatsApp QR Connector")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UAZAPI_BASE_URL = "https://benitechlab.uazapi.com"
active_sessions: Dict[str, dict] = {}

class ConnectRequest(BaseModel):
    instance_token: str = Field(..., min_length=1)
    phone: Optional[str] = Field(None)

class StatusRequest(BaseModel):
    instance_token: str = Field(..., min_length=1)

@app.get("/", response_class=HTMLResponse)
async def root():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Erro: index.html não encontrado</h1>", status_code=404)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "active_sessions": len(active_sessions),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/connect")
async def connect_whatsapp(request: ConnectRequest):
    logger.info(f"Iniciando conexão para instância: {request.instance_token[:8]}...")
    
    try:
        if len(request.instance_token) < 10:
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "Token inválido", "error": "invalid_token"}
            )
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "token": request.instance_token
        }
        
        body = {}
        if request.phone:
            phone = request.phone.strip().replace("+", "").replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
            if not phone.isdigit() or len(phone) < 10:
                return JSONResponse(
                    status_code=400,
                    content={"success": False, "message": "Número inválido", "error": "invalid_phone"}
                )
            body["phone"] = phone
            logger.info(f"Solicitando código de pareamento para: {phone}")
        else:
            logger.info("Solicitando QR Code")
        
        timeout = httpx.Timeout(30.0, connect=10.0)
        
        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                response = await client.post(
                    f"{UAZAPI_BASE_URL}/instance/connect",
                    headers=headers,
                    json=body if body else None
                )
                
                logger.info(f"Status da resposta: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    logger.info(f"RESPOSTA COMPLETA: {json.dumps(data, indent=2)}")
                    
                    active_sessions[request.instance_token] = {
                        "phone": body.get("phone", ""),
                        "type": "pairing" if body.get("phone") else "qr",
                        "created_at": datetime.now().isoformat()
                    }
                    
                    return {"success": True, "data": data, "message": "Conexão iniciada", "session_id": request.instance_token}
                
                elif response.status_code == 409:
                    logger.warning("Instância já está conectando")
                    return JSONResponse(
                        status_code=409,
                        content={"success": False, "message": "Instância já está em processo de conexão. Aguarde ou desconecte primeiro.", "error": "already_connecting"}
                    )
                
                elif response.status_code == 401:
                    return JSONResponse(status_code=401, content={"success": False, "message": "Token inválido ou expirado", "error": "invalid_token"})
                
                elif response.status_code == 404:
                    return JSONResponse(status_code=404, content={"success": False, "message": "Instância não encontrada", "error": "instance_not_found"})
                
                elif response.status_code == 429:
                    return JSONResponse(status_code=429, content={"success": False, "message": "Limite atingido. Aguarde.", "error": "rate_limit"})
                
                else:
                    logger.error(f"Status inesperado: {response.status_code}")
                    return JSONResponse(
                        status_code=response.status_code,
                        content={"success": False, "message": f"Erro {response.status_code}", "error": "unexpected_error", "details": response.text}
                    )
                    
            except httpx.TimeoutException:
                return JSONResponse(status_code=504, content={"success": False, "message": "Timeout", "error": "timeout"})
            except httpx.ConnectError:
                return JSONResponse(status_code=503, content={"success": False, "message": "Erro de conexão", "error": "connection_error"})
                    
    except Exception as e:
        logger.error(f"Erro: {str(e)}", exc_info=True)
        return JSONResponse(status_code=500, content={"success": False, "message": "Erro interno", "error": "internal_error"})

@app.post("/api/status")
async def check_status(request: StatusRequest):
    logger.info(f"Verificando status para: {request.instance_token[:8]}...")
    
    try:
        headers = {
            "Accept": "application/json",
            "token": request.instance_token
        }
        
        timeout = httpx.Timeout(15.0, connect=5.0)
        
        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                response = await client.get(f"{UAZAPI_BASE_URL}/instance/status", headers=headers)
                
                logger.info(f"Status code: {response.status_code}")
                
                if response.status_code == 200:
                    status_data = response.json()
                    logger.info(f"Status obtido: {status_data}")
                    
                    # A API retorna 'connected' e 'loggedIn'
                    is_connected = status_data.get('connected', False) and status_data.get('loggedIn', False)
                    
                    return {
                        "success": True,
                        "data": {
                            "status": "connected" if is_connected else "connecting",
                            "connected": status_data.get('connected', False),
                            "loggedIn": status_data.get('loggedIn', False),
                            "phone": status_data.get('jid', '').split('@')[0] if status_data.get('jid') else ""
                        }
                    }
                
                return JSONResponse(status_code=response.status_code, content={"success": False, "error": "status_error"})
                    
            except httpx.TimeoutException:
                return JSONResponse(status_code=504, content={"success": False, "error": "timeout"})
            except httpx.ConnectError:
                return JSONResponse(status_code=503, content={"success": False, "error": "connection_error"})
                
    except Exception as e:
        logger.error(f"Erro: {str(e)}", exc_info=True)
        return JSONResponse(status_code=500, content={"success": False, "error": "internal_error"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8010)
