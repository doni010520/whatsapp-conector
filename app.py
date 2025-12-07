from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import asyncio
from typing import Optional
import os
from datetime import datetime

app = FastAPI(title="WhatsApp QR Code Connector")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurações da UazAPI
UAZAPI_BASE_URL = "https://benitechlab.uazapi.com"

# Armazenar sessões ativas (em produção, use Redis ou banco de dados)
active_sessions = {}

class ConnectRequest(BaseModel):
    phone: Optional[str] = None
    instance_token: str

class StatusRequest(BaseModel):
    instance_token: str

@app.get("/", response_class=HTMLResponse)
async def root():
    """Página inicial com formulário"""
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/connect")
async def connect_whatsapp(request: ConnectRequest):
    """
    Conectar instância ao WhatsApp
    
    - Se phone for fornecido: gera código de pareamento
    - Se phone não for fornecido: gera QR code
    """
    try:
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {request.instance_token}"
        }
        
        payload = {}
        if request.phone:
            payload["phone"] = request.phone
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{UAZAPI_BASE_URL}/instance/connect",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Armazenar sessão
                session_id = request.instance_token
                active_sessions[session_id] = {
                    "phone": request.phone,
                    "status": "connecting",
                    "created_at": datetime.now().isoformat(),
                    "data": data
                }
                
                return {
                    "success": True,
                    "data": data,
                    "message": "Conexão iniciada com sucesso",
                    "session_id": session_id
                }
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Erro da UazAPI: {response.text}"
                )
                
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=408,
            detail="Timeout ao conectar com a UazAPI"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao conectar: {str(e)}"
        )

@app.post("/api/status")
async def check_status(request: StatusRequest):
    """
    Verificar status da conexão da instância
    """
    try:
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {request.instance_token}"
        }
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{UAZAPI_BASE_URL}/instance/status",
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Atualizar sessão se existir
                if request.instance_token in active_sessions:
                    active_sessions[request.instance_token]["status"] = data.get("status", "unknown")
                    active_sessions[request.instance_token]["last_check"] = datetime.now().isoformat()
                
                return {
                    "success": True,
                    "data": data
                }
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Erro da UazAPI: {response.text}"
                )
                
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=408,
            detail="Timeout ao verificar status"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao verificar status: {str(e)}"
        )

@app.get("/api/session/{session_id}")
async def get_session(session_id: str):
    """Obter informações da sessão"""
    if session_id in active_sessions:
        return {
            "success": True,
            "session": active_sessions[session_id]
        }
    else:
        raise HTTPException(
            status_code=404,
            detail="Sessão não encontrada"
        )

@app.delete("/api/session/{session_id}")
async def delete_session(session_id: str):
    """Remover sessão"""
    if session_id in active_sessions:
        del active_sessions[session_id]
        return {"success": True, "message": "Sessão removida"}
    else:
        raise HTTPException(
            status_code=404,
            detail="Sessão não encontrada"
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "active_sessions": len(active_sessions),
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8010))
    uvicorn.run(app, host="0.0.0.0", port=port)
