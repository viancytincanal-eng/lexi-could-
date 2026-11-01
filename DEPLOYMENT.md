# Despliegue cloud sin tarjeta: Render + Neon

## Diseño

- **Render Free:** ejecuta el contenedor Docker de FastAPI y sirve la interfaz por HTTPS.
- **Neon Free:** PostgreSQL externo para que conversaciones y mensajes sobrevivan a reinicios y suspensiones de Render.
- **Proveedor LLM:** cualquier endpoint compatible con OpenAI Chat Completions; se configura después, sin exponer la clave al navegador.

## Límites que debemos aceptar

### Render Free
- 512 MB RAM y CPU compartida limitada.
- El servicio se duerme tras 15 minutos sin tráfico y tarda aproximadamente un minuto en arrancar de nuevo.
- El sistema de archivos local es efímero y no debe guardar la memoria.
- Los servicios gratuitos pueden reiniciarse y tienen límites de uso/compilación.

### Neon Free
- Plan gratuito permanente, sin tarjeta de crédito.
- 1 GB de almacenamiento por proyecto.
- 100 CU-hours mensuales por proyecto y 5 GB de transferencia pública según los límites actuales.
- El cómputo se suspende tras inactividad; la primera consulta lo despierta.
- Si se alcanza el límite de cómputo o transferencia, la base puede suspenderse hasta el siguiente período. Los datos permanecen almacenados.

## Pasos

1. Crear cuenta en Neon: https://console.neon.tech/signup
2. Crear un proyecto PostgreSQL y copiar la cadena de conexión (botón Connect).
3. Crear cuenta en Render: https://render.com/
4. En Render, seleccionar New > Blueprint y conectar el repositorio público `viancytincanal-eng/lexi-could-`.
5. Render leerá `render.yaml`. En el formulario del Blueprint, completar los valores secretos que aparecen como `sync: false`.
6. Para `DATABASE_URL`, pegar la cadena de Neon completa. Mantenerla privada.
7. Para `LLM_BASE_URL`, `LLM_MODEL` y `LLM_API_KEY`, se puede dejar vacío inicialmente; el servicio arrancará, pero el chat no responderá hasta configurar un modelo.
8. Desplegar. Render generará `APP_TOKEN` automáticamente. Copiarlo desde Environment y guardarlo en un lugar privado.
9. Abrir la URL HTTPS de la aplicación, entrar en Ajustes y pegar el token.

## Importante

- No enviar contraseñas, claves API, tokens ni cadenas de conexión por el chat.
- No guardar credenciales en GitHub.
- No convertir el plan de Render o Neon a uno de pago sin revisar primero los costos.
- Este documento describe el procedimiento; el servicio todavía no está desplegado.
- Antes de invitar a otras personas, implementar cuentas individuales, rate limiting, borrado/exportación de datos y copias de seguridad.
