# Redes en Docker

## Los tres tipos de red nativos

**bridge** es la red por defecto. Los contenedores se conectan a un switch
virtual interno y pueden comunicarse entre ellos por IP. El host accede a ellos
mediante mapeo de puertos. Es el tipo más usado en desarrollo y en Docker Compose.

**host** elimina el aislamiento de red: el contenedor usa directamente la interfaz
de red del host, sin traducción de puertos. Más rendimiento, menos aislamiento.
Se usa cuando la aplicación necesita acceso de red de muy baja latencia.

**none** desactiva completamente la red del contenedor. No tiene interfaz de red
salvo el loopback. Se usa para contenedores que procesan datos localmente y no
necesitan comunicación externa.

## Service discovery en Docker Compose

Cuando varios servicios están en la misma red de Compose, Docker crea un servidor
DNS interno automáticamente. Cada servicio es accesible por su nombre tal como
está definido en el docker-compose.yml. Por eso en nuestro caso el backend puede
conectarse a Redis usando simplemente `redis` como hostname, sin conocer su IP.

## Puerto publicado vs puerto expuesto internamente

Un puerto **publicado** abre el puerto en el host y lo hace
accesible desde fuera del sistema. Cualquier persona en la red puede llegar a él.

Un puerto **expuesto internamente** solo es visible para
otros contenedores dentro de la misma red Docker. No es accesible desde el host
ni desde internet. Es más seguro para servicios que solo deben comunicarse
internamente, como nuestra API detrás de NGINX.