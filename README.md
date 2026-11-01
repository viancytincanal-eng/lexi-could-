# Lexi Cloud

Asistente conversacional independiente, alojada en la nube y accesible desde móvil.

## Objetivo

Construir una aplicación propia con interfaz web adaptable, backend propio, memoria persistente y un modelo de lenguaje intercambiable.

## Estado actual: prototipo 0.1

- Interfaz web móvil.
- API FastAPI.
- Memoria persistente de conversaciones con SQLite.
- Adaptador para modelos con API compatible con OpenAI Chat Completions.
- Configuración mediante variables de entorno.
- Dockerfile y Docker Compose para despliegue.
- Sin claves reales ni secretos guardados en el repositorio.

## Inicio rápido

1. Copia `.env.example` como `.env` en el servidor.
2. Configura un token largo en `APP_TOKEN`.
3. Configura `LLM_BASE_URL`, `LLM_MODEL` y `LLM_API_KEY` según el proveedor elegido.
4. Ejecuta `docker compose up --build -d`.
5. Abre el servidor por HTTPS y pega el token en Ajustes.

No publiques el servicio sin HTTPS y sin cambiar el token de ejemplo.

## Estructura

- `frontend/`: interfaz móvil.
- `backend/app/`: API, memoria y adaptador del modelo.
- `ARCHITECTURE.md`: decisiones, límites y siguientes pasos.

## Principios

- Evitar depender de un único proveedor.
- Mantener el código y los datos bajo nuestro control.
- Separar personalidad, memoria y conocimiento documental.
- Mantener las claves API y secretos fuera del repositorio.
