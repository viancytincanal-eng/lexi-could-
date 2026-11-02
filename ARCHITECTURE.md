# Arquitectura de Lexi Cloud 0.2

## Flujo
Navegador móvil -> FastAPI propio -> PostgreSQL/SQLite para conversaciones -> adaptador de proveedor compatible con OpenAI Chat Completions.

## Componentes
- `frontend/index.html`: interfaz móvil y centro de motores.
- `backend/app/main.py`: API, autenticación y prueba de conexiones.
- `backend/app/db.py`: conversaciones y mensajes persistentes.
- `backend/app/llm.py`: adaptador desacoplado y validación HTTPS de proveedores.
- `backend/app/config.py`: configuración del servidor.

## Centro de motores (fase inicial)
- El usuario puede elegir Gemini, Groq, OpenRouter o un endpoint compatible admitido.
- La interfaz permite probar el proveedor antes de conversar.
- La URL y el modelo se guardan en el navegador; la clave API permanece en sessionStorage y se envía al backend solo al probar o conversar.
- Las claves de proveedores no se guardan en la base de datos ni en GitHub.
- El servidor admite inicialmente los hosts oficiales de Google Gemini, Groq, OpenRouter y OpenAI.
- Se usa HTTPS y se rechazan hosts no incluidos en la lista de confianza para reducir riesgos de SSRF.

## Límites conocidos
- El formato de conversación debe ser compatible con OpenAI Chat Completions. El endpoint Gemini `/v1beta/interactions` no es compatible con este adaptador; se utiliza el endpoint de compatibilidad OpenAI de Gemini.
- No existe todavía descubrimiento automático de proveedores, catálogo verificado de cuotas gratuitas ni cambio automático entre proveedores.
- La clave API se conserva solo durante la sesión de la pestaña; si se cierra, habrá que introducirla de nuevo.
- No hay todavía generación de imágenes/vídeos, voz, multiusuario, RAG, streaming ni exportación/borrado de conversaciones.
- La autenticación sigue usando un único APP_TOKEN compartido y es apropiada solo para pruebas privadas.

## Próximas fases
1. Verificar el despliegue 0.2 y conectar el primer proveedor.
2. Añadir catálogo de modelos con disponibilidad y límites comprobados.
3. Añadir perfiles de proveedores múltiples y fallback con límites seguros.
4. Incorporar adaptadores independientes de imagen, vídeo y voz.
5. Mejorar autenticación, gestión de secretos, copias de seguridad y privacidad antes de uso público.
