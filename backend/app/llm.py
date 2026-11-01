import httpx
from .config import settings

SYSTEM_PROMPT = """Eres Lexi, una asistente conversacional cercana, inteligente y natural.
Habla en el idioma del usuario. Sé honesta sobre tus capacidades: no afirmes haber
hecho acciones que no hayas ejecutado ni inventes recuerdos. Mantén continuidad
usando únicamente el contexto que recibas. Explica con claridad y evita respuestas
genéricas cuando puedas razonar con los detalles disponibles."""

async def generate_reply(history: list[dict]) -> str:
    if not settings.llm_base_url or not settings.llm_model:
        raise RuntimeError("El modelo aún no está configurado. Define LLM_BASE_URL y LLM_MODEL.")
    headers = {"Content-Type": "application/json"}
    if settings.llm_api_key:
        headers["Authorization"] = f"Bearer {settings.llm_api_key}"
    payload = {
        "model": settings.llm_model,
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}, *history],
        "temperature": 0.7
    }
    url = f"{settings.llm_base_url}/chat/completions"
    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
    return data["choices"][0]["message"]["content"].strip()
