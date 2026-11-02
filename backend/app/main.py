import secrets
import uuid
import httpx
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .config import settings
from .db import add_message, ensure_conversation, get_messages, init_db, list_conversations
from .llm import generate_reply, validate_provider_url

app = FastAPI(title=settings.app_name, version="0.2.0")
FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"


@app.on_event("startup")
def startup():
    init_db()


@app.middleware("http")
async def protect_api(request: Request, call_next):
    if request.url.path.startswith("/api/") and request.url.path != "/api/health":
        from starlette.responses import JSONResponse
        if not settings.api_token:
            return JSONResponse(status_code=503, content={"detail": "El servidor aún no tiene APP_TOKEN configurado"})
        supplied = request.headers.get("authorization", "")
        expected = f"Bearer {settings.api_token}"
        if not secrets.compare_digest(supplied, expected):
            return JSONResponse(status_code=401, content={"detail": "No autorizado"})
    return await call_next(request)


class ProviderConfig(BaseModel):
    base_url: str = Field(min_length=8, max_length=500)
    model: str = Field(min_length=1, max_length=200)
    api_key: str = Field(min_length=1, max_length=2000)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=12000)
    conversation_id: str | None = None
    provider: ProviderConfig


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "model_configured": False,
        "provider_mode": "client_supplied",
        "auth_configured": bool(settings.api_token),
    }


@app.post("/api/providers/test")
async def test_provider(provider: ProviderConfig):
    try:
        validate_provider_url(provider.base_url)
        reply = await generate_reply(
            [{"role": "user", "content": "Responde únicamente: conexión correcta."}],
            provider.model_dump(),
        )
        return {"ok": True, "model": provider.model, "message": reply[:160]}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except httpx.HTTPStatusError as exc:
        status = exc.response.status_code
        if status in (401, 403):
            detail = "El proveedor rechazó la clave API. Comprueba que sea correcta."
        elif status == 429:
            detail = "El proveedor alcanzó su límite de uso. Prueba más tarde o con otro modelo."
        else:
            detail = f"El proveedor devolvió un error HTTP {status}."
        raise HTTPException(status_code=502, detail=detail) from exc
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail="No se pudo contactar con el proveedor.") from exc


@app.get("/api/conversations")
def conversations():
    return {"conversations": list_conversations()}


@app.get("/api/conversations/{conversation_id}/messages")
def conversation_messages(conversation_id: str):
    return {"conversation_id": conversation_id, "messages": get_messages(conversation_id, 500)}


@app.post("/api/chat")
async def chat(body: ChatRequest):
    conversation_id = body.conversation_id or str(uuid.uuid4())
    ensure_conversation(conversation_id)
    add_message(conversation_id, "user", body.message.strip())
    history = get_messages(conversation_id, settings.max_history_messages)
    try:
        reply = await generate_reply(history, body.provider.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except httpx.HTTPStatusError as exc:
        status = exc.response.status_code
        if status in (401, 403):
            detail = "El proveedor rechazó la clave API. Revísala en Ajustes."
        elif status == 429:
            detail = "El proveedor alcanzó su límite gratuito. Podremos cambiar a otro proveedor desde Ajustes."
        else:
            detail = f"El proveedor devolvió un error HTTP {status}."
        raise HTTPException(status_code=502, detail=detail) from exc
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail="No se pudo contactar con el proveedor.") from exc
    add_message(conversation_id, "assistant", reply)
    return {"conversation_id": conversation_id, "reply": reply}


@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")


app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
