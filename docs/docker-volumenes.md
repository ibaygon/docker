# Volúmenes en Docker

## Por qué los volúmenes son necesarios

Los contenedores son efímeros. Todo lo escrito en su sistema de archivos
desaparece al eliminarlos. Los volúmenes son directorios gestionados por Docker
que viven fuera del ciclo de vida del contenedor y persisten aunque este se
elimine y se vuelva a crear.

## Volumen nombrado vs bind mount

Un **volumen nombrado** es gestionado completamente por
Docker. Docker decide dónde almacenarlo en el host. Es la opción recomendada
para datos de servicios como Redis o bases de datos porque Docker gestiona
permisos y portabilidad.

Un **bind mount** monta una carpeta concreta del host
dentro del contenedor. El desarrollador controla la ubicación exacta. Es útil
durante el desarrollo para que los cambios en el código se reflejen
inmediatamente sin reconstruir la imagen.

En nuestro proyecto usamos ambos: volumen nombrado para los datos de Redis y
bind mount para la carpeta data de la API, de forma que los archivos CSV y
los logs del host estén disponibles dentro del contenedor.