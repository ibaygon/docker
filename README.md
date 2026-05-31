# Docker Toolkit

Infraestructura containerizada para el sys-admin toolkit construida con Docker.

Aplicación FastAPI dockerizada con tres servicios orquestados mediante Docker
Compose: backend Python, caché Redis y proxy inverso NGINX. Arranca completamente
con un solo comando y es accesible en el puerto 80.
 
Repositorio: https://github.com/ibaygon/docker 

---

## Características

1. API REST con FastAPI que expone endpoints para auditoría de logs SSH, geolocalización de IPs y análisis de inventarios de red
2. Caché con Redis que almacena los resultados del parseo de logs durante 60 segundos, reduciendo el procesamiento repetido
3. Infraestructura completa con NGINX como proxy inverso, rate limiting de 10 requests por segundo y healthchecks en todos los servicios

---

## Tecnologías

### Backend
Tecnología: Uso 
Python 3.11 Alpine: Imagen base ligera para el contenedor de la API
FastAPI: Framework web con Swagger UI automático en /docs
Uvicorn: Servidor ASGI que ejecuta la aplicación dentro del contenedor

### Infraestructura
Tecnología: Uso
Docker Compose: Orquestación de los tres servicios con dependencias y healthchecks
Redis 7 Alpine: Caché de resultados y almacenamiento de IPs sospechosas con estructuras SET
NGINX Alpine: Proxy inverso con rate limiting que expone el puerto 80 al exterior

### Auxiliares
Tecnología: Uso 
Pandas: Análisis y filtrado del inventario CSV dentro del contenedor
Faker: Generación de inventarios ficticios de 1000 servidores
python-dotenv: Lectura de variables de entorno desde el archivo .env

---

## Estructura del proyecto

La raíz contiene los archivos de configuración de la infraestructura y los módulos Python.

**Archivos de la API** — main.py es el punto de entrada de FastAPI con todos los endpoints. log_parser.py, inventory_manager.py y generate_inventory.py son los módulos del toolkit importados por la API.

**Configuración Docker** — Dockerfile construye la imagen en 5 capas usando Python Alpine. docker-compose.yml define los tres servicios, la red interna toolkit-net y el volumen redis-data. nginx.conf configura el proxy inverso con rate limiting y las cabeceras correctas.

**Configuración de entorno** — .env contiene las credenciales reales y no se sube a Git. .env.example es la plantilla pública. .dockerignore excluye archivos innecesarios del contexto de build.

**Datos y documentación** — la carpeta data contiene auth.log y el inventory.csv generado en tiempo de ejecución. La carpeta docs contiene los cuatro documentos teóricos sobre Docker, redes, volúmenes y NGINX.

---

## Descargar y ejecutar

```bash
git clone https://github.com/ibaygon/docker.git
cd docker
```

Crea el archivo `.env` con tus credenciales:

```bash
cp .env.example .env
# edita .env y pon tu REDIS_PASSWORD
```

Levanta toda la infraestructura con un solo comando:

```bash
docker-compose up --build
```

Genera el inventario de ejemplo:

```bash
docker-compose run --rm backend python generate_inventory.py
```

Abre en el navegador:

- `http://localhost/docs` — Swagger UI completo
- `http://localhost/health` — estado de API y Redis
- `http://localhost/logs/attackers` — IPs atacantes con caché Redis
- `http://localhost/inventory` — análisis del inventario

---

## Comandos útiles

```bash
docker-compose ps                                     
docker stats                                         
docker exec -it toolkit-redis redis-cli -a PASSWORD  
docker-compose logs -f backend                       
docker-compose down                                  
docker system prune -a --volumes                     
# limpiar recursos (~424MB)
```

---

## Desarrollado durante las prácticas en Corner Estudios — Pietro Simonato — 2026