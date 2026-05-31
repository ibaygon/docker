# Docker 

## Máquina virtual vs contenedor

Una máquina virtual es como una computadora completa. Tiene su propio sistema operativo y emula todo el hardware. Esto significa que consume mucha memoria, varios gigas, y tarda minutos en arrancar. Esto se debe a que virtualiza la CPU, la memoria y el disco a nivel de hardware mediante un hipervisor.

Un contenedor es diferente. No virtualiza hardware, sino que comparte el kernel del sistema operativo del host. Solo aísla procesos mediante namespaces y cgroups del propio kernel de Linux. Esto hace que arranque muy rápido, en milisegundos, y ocupe muy poca memoria, solo megas.

**Qué comparte el contenedor con el host:** el kernel de Linux, los drivers del hardware y los recursos físicos como la CPU y la RAM, gestionados por cgroups.

**Qué aísla:** el sistema de archivos, los procesos, la red, los usuarios y las variables de entorno.

## Conceptos clave

**Imagen:** es una plantilla de solo lectura que contiene el sistema de archivos y la configuración necesaria para ejecutar una aplicación. Es inmutable, es decir, no se puede cambiar.

**Contenedor:** es una instancia en ejecución de una imagen. Es efímero por defecto, lo que significa que cuando se detiene, se elimina.

**Dockerfile:** es un archivo de texto con instrucciones para construir una imagen capa a capa de forma reproducible.

**Docker Hub:** es el registro público oficial donde se almacenan y distribuyen imágenes.

**Capa:** cada instrucción del Dockerfile genera una capa inmutable. Docker reutiliza las capas cacheadas para acelerar los builds posteriores.

**Registro:** es un servidor que almacena imágenes. Docker Hub es el público por defecto, pero existen registros privados como GitHub Container Registry o AWS ECR.

## Ciclo de vida de un contenedor

1. **Creado:** el contenedor existe pero no ha arrancado. Se utiliza el comando `docker create`.

2. **En ejecución:** el proceso principal está activo. Se utilizan los comandos `docker start` o `docker run`.

3. **Pausado:** los procesos están congelados con SIGSTOP. Se utiliza el comando `docker pause`.

4. **Detenido:** el proceso principal ha terminado o fue detenido. Se utiliza el comando `docker stop`.

5. **Eliminado:** el contenedor desaparece del sistema. Se utiliza el comando `docker rm`.

**Qué ocurre con los datos al eliminar un contenedor:** se pierden. Todo lo escrito en el sistema de archivos del contenedor desaparece con él. Para persistir datos, se usan volúmenes o bind mounts que viven fuera del ciclo de vida del contenedor.

## Relación kernel, Docker Engine y contenedores

El kernel del host provee namespaces y cgroups. Docker Engine es un demonio que actúa como intermediario: recibe comandos del cliente Docker, gestiona imágenes y crea contenedores usando las primitivas del kernel. Los contenedores son procesos aislados que corren directamente sobre ese kernel compartido, sin capa de virtualización intermedia.

```

┌─────────────────────────────────────┐

│           Docker Client             │

│         (docker run, build...)      │

└────────────────┬────────────────────┘

│ API REST

┌────────────────▼────────────────────┐

│           Docker Engine             │

│    (dockerd + containerd + runc)    │

└──────┬──────────────┬───────────────┘

│              │

┌──────▼──────┐ ┌─────▼───────┐

│ Contenedor 1│ │Contenedor 2 │

│  (proceso)  │ │  (proceso)  │

└──────┬──────┘ └─────┬───────┘

│              │

┌──────▼──────────────▼───────────────┐

│        Kernel del Host (Linux)      │

│     namespaces · cgroups · runc     │

└─────────────────────────────────────┘

```