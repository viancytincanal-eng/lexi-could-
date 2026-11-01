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

1. Crear un proyecto PostgreSQL en Neon.
2. En Render, seleccionar **New > Blueprint** y conectar el repositorio público `viancytincanal-eng/lexi-could-`.
3. Render leerá `render.yaml`. En el formulario inicial, completar únicamente `DATABASE_URL` con la cadena privada de Neon.
4. Render generará automáticamente `APP_TOKEN`. No hace falta inventarlo ni guardarlo en GitHub.
5. Aplicar el Blueprint y esperar a que el servicio quede Live.
6. Abrir la URL HTTPS de la aplicación. Copiar `APP_TOKEN` desde el apartado Environment de Render y pegarlo en Ajustes dentro de Lexi Cloud.
7. El servidor y la memoria quedarán conectados, pero el chat todavía no responderá hasta que configuremos un modelo en `LLM_BASE_URL`, `LLM_MODEL` y, si el proveedor lo requiere, `LLM_API_KEY`. Esas variables se añadirán después desde Render, cuando elijamos el modelo.

## Importante

- No enviar contraseñas, claves API, tokens ni cadenas de conexión por el chat.
- No guardar credenciales en GitHub.
- No convertir el plan de Render o Neon a uno de pago sin revisar primero los costos.
- El servicio todavía no está desplegado.
- Antes de invitar a otras personas, implementar cuentas individuales, rate limiting, borrado/exportación de datos y copias de seguridad.
