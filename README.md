# Lexi Cloud

Asistente conversacional independiente, alojada en la nube y accesible desde móvil.

## Estado actual: prototipo 0.2
- Interfaz web móvil con centro de motores.
- API FastAPI.
- Memoria persistente de conversaciones en SQLite o PostgreSQL.
- Adaptador de proveedores compatibles con OpenAI Chat Completions.
- Prueba de conexión desde la interfaz.
- Proveedores iniciales: Gemini (compatibilidad OpenAI), Groq, OpenRouter y OpenAI.
- Las claves API de proveedores no se guardan en GitHub ni en la base de datos; se mantienen en la sesión del navegador y se envían al backend por HTTPS.

## Importante
El centro de motores es una primera versión. Todavía no descubre automáticamente modelos ni conmuta por sí solo entre proveedores. La disponibilidad gratuita y las cuotas dependen de cada proveedor y deben comprobarse antes de elegir un modelo.

Gemini debe configurarse con su endpoint compatible con OpenAI; la ruta `/v1beta/interactions` no es compatible con el adaptador actual.

## Despliegue
El proyecto conserva el despliegue actual y la base de datos configurada. No publiques claves API, tokens ni cadenas de conexión en GitHub. Consulta `DEPLOYMENT.md` para los detalles del entorno.

## Estructura
- `frontend/`: interfaz móvil.
- `backend/app/`: API, memoria y adaptadores.
- `ARCHITECTURE.md`: diseño, seguridad y fases pendientes.
- `DEPLOYMENT.md`: notas de despliegue.
