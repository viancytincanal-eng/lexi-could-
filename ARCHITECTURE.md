# Arquitectura de Lexi Cloud 0.1

## Flujo
Navegador móvil -> FastAPI propio -> memoria SQLite + adaptador LLM OpenAI-compatible.

## Componentes
- `frontend/index.html`: interfaz web adaptable.
- `backend/app/main.py`: API, autenticación opcional por token y rutas.
- `backend/app/db.py`: conversaciones y mensajes persistentes.
- `backend/app/llm.py`: adaptador desacoplado del proveedor.
- `backend/app/config.py`: configuración por variables de entorno.

## Decisiones
- El navegador nunca recibe la clave del proveedor del modelo.
- La memoria local del servidor no depende del proveedor LLM.
- El endpoint del modelo se puede cambiar mediante variables de entorno.
- SQLite sirve para el prototipo de una instancia; PostgreSQL será mejor al escalar.
- Imágenes, voz y vídeo se añadirán como adaptadores independientes.

## Límites actuales
- No hay registro de usuarios ni multiusuario.
- La autenticación es un único token compartido, adecuado sólo para pruebas privadas.
- No hay streaming, recuperación documental (RAG), borrado/exportación de datos ni límites de uso.
- El modelo debe ofrecer una API compatible con `/chat/completions`.
- El despliegue público requiere HTTPS, token fuerte, copias de seguridad y revisión de seguridad.

## Siguiente fase
1. Elegir hosting y proveedor de inferencia.
2. Desplegar en entorno privado con HTTPS.
3. Verificar persistencia y seguridad.
4. Añadir cuentas individuales, gestión de memoria y PostgreSQL.
