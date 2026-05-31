# NGINX como proxy inverso

## Proxy inverso vs proxy directo

Un proxy directo actúa en nombre del cliente: el cliente le pide al proxy que
acceda a internet por él. Se usa para anonimizar tráfico o filtrar contenido
en redes corporativas.

Un proxy inverso actúa en nombre del servidor: el cliente habla con NGINX sin
saber que hay una aplicación detrás. NGINX decide a qué servidor interno
reenviar la petición.

## Por qué NGINX delante de la aplicación en producción

Uvicorn no está diseñado para exponerse directamente a internet. NGINX añade
capas esenciales: gestiona SSL/TLS para HTTPS, aplica rate limiting para
bloquear ataques de fuerza bruta, sirve archivos estáticos sin tocar Python,
y puede cachear respuestas para reducir carga en el backend.

## Upstream y server block

**upstream** define un grupo de servidores backend. NGINX puede balancear
carga entre varios. En nuestro caso apunta a `backend:8000`, usando el nombre
del servicio Docker como hostname gracias al DNS interno de Compose.

**server block** define cómo NGINX escucha y responde: en qué puerto, qué
locations maneja y hacia qué upstream hace proxy_pass.

## NGINX vs Apache bajo carga

NGINX usa un modelo asíncrono y no bloqueante con un número fijo de workers.
Cada worker maneja miles de conexiones simultáneas con un solo hilo.
Apache usa un proceso o hilo por conexión, lo que limita la concurrencia
y consume más memoria bajo carga alta. Por eso NGINX es el estándar en
infraestructuras de alto tráfico.