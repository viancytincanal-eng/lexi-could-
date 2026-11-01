# Lexi Cloud

Asistente conversacional independiente, alojada en la nube y accesible desde móvil.

## Estado actual: prototipo 0.1

- Interfaz web móvil.
- API FastAPI.
- Memoria persistente: SQLite local o PostgreSQL externo.
- Adaptador para modelos con API compatible con OpenAI Chat Completions.
- Configuración mediante variables de entorno.
- Dockerfile y blueprint de despliegue para Render.
- Sin claves reales ni secretos guardados en el repositorio.

## Despliegue sin tarjeta (propuesta inicial)

1. Crear una base PostgreSQL gratuita en Neon.
2. Crear una cuenta gratuita en Render y conectar este repositorio.
3. Render detecta `render.yaml` y prepara el servicio Docker.
4. En Render, introducir la URL privada de Neon en `DATABASE_URL`.
5. Configurar el proveedor/modelo en `LLM_BASE_URL`, `LLM_MODEL` y `LLM_API_KEY`.
6. Desplegar y abrir la URL HTTPS de Render.

El servicio gratuito de Render se duerme tras inactividad y su disco local es efímero. Por eso la memoria se guarda en Neon, no en el contenedor. La base gratuita de Neon tiene límites de almacenamiento y cómputo; revisar `DEPLOYMENT.md`.

## Inicio local

Configura `.env` con un `APP_TOKEN` largo y, si quieres conversar, los datos del modelo. Ejecuta:

```bash
docker compose up --build
```

## Seguridad

- El navegador nunca recibe la clave del proveedor del modelo.
- La API requiere `APP_TOKEN`; el endpoint de salud es público para los chequeos del hosting.
- Nunca subas `.env` ni claves reales a GitHub.
- Antes de uso público, añade cuentas individuales, copias de seguridad y controles de abuso.

## Estructura

- `frontend/`: interfaz móvil.
- `backend/app/`: API, memoria y adaptador del modelo.
- `render.yaml`: configuración inicial de despliegue.
- `ARCHITECTURE.md`: decisiones técnicas.
- `DEPLOYMENT.md`: pasos y límites del alojamiento.

## Principios

- Evitar depender de un único proveedor.
- Mantener el código y los datos bajo nuestro control.
- Separar personalidad, memoria y conocimiento documental.
