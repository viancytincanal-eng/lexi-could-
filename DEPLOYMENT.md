# Despliegue recomendado

## Objetivo
Mantener la aplicación y la memoria en una máquina virtual propia, y usar un proveedor intercambiable sólo para la inferencia del modelo. No ejecutar el modelo grande en el teléfono.

## Opción recomendada para empezar: Oracle Cloud Always Free
Oracle publica recursos Always Free que no caducan, incluyendo hasta 2 OCPU y 12 GB de RAM en Ampere A1, más almacenamiento de volúmenes dentro de los límites gratuitos. La instancia debe crearse en la región principal de la cuenta. Puede haber falta temporal de capacidad y Oracle puede reclamar instancias que considere inactivas.

Antes de elegirla:
- La mayoría de los registros requieren teléfono y tarjeta para verificación.
- La tarjeta no debería recibir cargos salvo que se convierta la cuenta a modalidad de pago o se excedan los límites gratuitos.
- No se debe pulsar Upgrade ni crear recursos que no estén marcados Always Free Eligible.
- La región principal no se puede cambiar después.

## Modelo inicial de prueba: OpenRouter
El backend usa una API compatible con OpenAI Chat Completions. Para probar una ruta gratuita de modelos abiertos, los valores iniciales pueden ser:

- `LLM_BASE_URL=https://openrouter.ai/api/v1`
- `LLM_MODEL=openrouter/free`
- `LLM_API_KEY=` tu clave privada de OpenRouter

La ruta gratuita está limitada y puede elegir entre modelos gratuitos disponibles; no es una garantía de modelo fijo ni de servicio ilimitado. OpenRouter publica un límite base de 20 solicitudes por minuto y 50 por día para variantes gratuitas. Las condiciones pueden cambiar.

## Variables de entorno
Configura `APP_TOKEN` con un secreto largo y aleatorio. No reutilices contraseñas personales. Mantén `.env` fuera de GitHub. Nunca escribas claves del proveedor en el frontend.

## Seguridad antes de abrir al público
- HTTPS obligatorio.
- Token privado fuerte.
- Firewall: exponer sólo los puertos necesarios.
- Copias de seguridad de `/data` (contiene SQLite).
- No compartir el token en capturas, mensajes públicos ni el repositorio.

## Alternativas descartadas para memoria persistente
Render Free puede servir para una demostración, pero apaga el servicio tras 15 minutos sin tráfico y elimina los archivos locales al dormir, reiniciar o desplegar. Su base Postgres gratuita tiene límite de 30 días. No es una buena ubicación para conservar la memoria de Lexi a largo plazo.

## Estado
Este documento es un plan, no una confirmación de despliegue. No se ha creado una cuenta cloud, VM, clave API ni servicio público.
