import secrets
import uuid
from pathlib import Path
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .config import settings
from .db import add_message, ensure_conversation, get_messages, init_db, list_conversations
from .llm import generate_reply

app = FastAPI(title=settings.app_name, version="0.1.0")
FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"

@app.on_event("startup")
def startup():
    init_db()

@app.middleware("http")
async def protect_api(request, call_next):
    if request.url.path.startswith("/api/") and request.url.path != "/api/health":
        from starlette.responses import JSONResponse
        if not settings.api_token:
            return JSONResponse(status_code=503, content={"detail": "El servidor aún no tiene APP_TOKEN configurado"})
        supplied = request.headers.get("authorization", "")
        expected = f"Bearer {settings.api_token}"
        if not secrets.compare_digest(supplied, expected):
            return JSONResponse(status_code=401, content={"detail": "No autorizado"})
    return await call_next(request)

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=12000)
    conversation_id: str | None = None

@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "model_configured": bool(settings.llm_base_url and settings.llm_model),
        "auth_configured": bool(settings.api_token)
    }

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
        reply = await generate_reply(history)
    except httpx_error_types() as exc:
        raise HTTPException(status_code=502, detail=f"Error al consultar el modelo: {exc}") from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    add_message(conversation_id, "assistant", reply)
    return {"conversation_id": conversation_id, "reply": reply}

def httpx_error_types():
    import httpx
    return (httpx.HTTPError, KeyError, ValueError, IndexError)

@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
