import ipaddress
from urllib.parse import urlparse

import httpx

SYSTEM_PROMPT = """Eres Lexi, una asistente conversacional cercana, inteligente y natural.
Habla en el idioma del usuario. Sé honesta sobre tus capacidades: no afirmes haber
hecho acciones que no hayas ejecutado ni inventes recuerdos. Mantén continuidad
usando únicamente el contexto que recibas. Explica con claridad y evita respuestas
genéricas cuando puedas razonar con los detalles disponibles."""

ALLOWED_API_HOSTS = {
    "generativelanguage.googleapis.com",
    "api.groq.com",
    "openrouter.ai",
    "api.openai.com",
}


def validate_provider_url(base_url: str) -> str:
    value = base_url.strip().rstrip("/")
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("La dirección del proveedor debe ser HTTPS y no incluir credenciales.")
    host = parsed.hostname.lower()
    try:
        address = ipaddress.ip_address(host)
        if not address.is_global:
            raise ValueError("No se permiten direcciones locales o privadas.")
    except ValueError as exc:
        if "does not appear to be an IPv4 or IPv6 address" not in str(exc):
            raise
        if host not in ALLOWED_API_HOSTS:
            raise ValueError("Por seguridad, este proveedor aún no está en la lista de conexiones admitidas.")
    return value


async def generate_reply(history: list[dict], provider: dict) -> str:
    base_url = validate_provider_url(provider.get("base_url", ""))
    model = provider.get("model", "").strip()
    api_key = provider.get("api_key", "").strip()
    if not model:
        raise ValueError("Escribe el identificador exacto del modelo.")
    if not api_key:
        raise ValueError("Falta la clave API del proveedor.")
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}, *history],
        "temperature": 0.7,
    }
    async with httpx.AsyncClient(timeout=90, follow_redirects=False) as client:
        response = await client.post(f"{base_url}/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError, AttributeError) as exc:
        raise ValueError("El proveedor respondió en un formato que Lexi todavía no reconoce.") from exc
