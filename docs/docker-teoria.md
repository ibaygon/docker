# Docker

## Máquina virtual vs contenedor

Una máquina virtual es como una computadora completa. Tiene su propio sistema operativo y emula todo el hardware. Esto significa que consume mucha memoria y tarda minutos en arrancar. Esto se debe a que virtualiza la CPU, la memoria y el disco a nivel de hardware mediante un hipervisor.

Un contenedor es diferente. No virtualiza hardware, sino que comparte el kernel del sistema operativo del host. Solo aísla procesos mediante namespaces y cgroups del propio kernel de Linux. Esto hace que arranque muy rápido y ocupe muy poca memoria.

**Qué comparte el contenedor con el host:** el kernel de Linux, los drivers del hardware y los recursos físicos como la CPU y la RAM.

**Qué aísla:** el sistema de archivos, los procesos, la red, los usuarios y las variables de entorno.

## Conceptos clave

**Imagen:** es una plantilla de solo lectura que contiene el sistema de archivos y la configuración necesaria para ejecutar una aplicación. No se puede cambiar.

**Contenedor:** es una instancia en ejecución de una imagen. Desaparece cuando se detiene.

**Dockerfile:** es un archivo de texto con instrucciones para construir una imagen.

**Docker Hub:** es el lugar donde se almacenan y distribuyen imágenes.

**Capa:** cada instrucción del Dockerfile genera una capa inmutable. Docker reutiliza las capas para acelerar los builds.

**Registro:** es un servidor que almacena imágenes. Docker Hub es el público por defecto.

## Ciclo de vida de un contenedor

1. **Creado:** el contenedor existe pero no ha arrancado. Se utiliza el comando `docker create`.

2. **En ejecución:** el proceso principal está activo. Se utilizan los comandos `docker start` o `docker run`.

3. **Pausado:** los procesos están congelados.

4. **Detenido:** el proceso principal ha terminado o fue detenido. Se utiliza el comando `docker stop`.

5. **Eliminado:** el contenedor desaparece del sistema. Se utiliza el comando `docker rm`.

**Qué ocurre con los datos al eliminar un contenedor:** se pierden. Para persistir datos, se usan volúmenes o bind mounts.

## Relación kernel, Docker Engine y contenedores

El kernel del host provee namespaces y cgroups. Docker Engine actúa como intermediario: recibe comandos, gestiona imágenes y crea contenedores. Los contenedores son procesos aislados que corren directamente sobre el kernel compartido.

El kernel del host provee namespaces y cgroups. Docker Engine actúa como intermediario entre el cliente y el kernel: recibe los comandos, gestiona las imágenes y arranca los contenedores. Los contenedores son procesos aislados que corren sobre el kernel compartido.
