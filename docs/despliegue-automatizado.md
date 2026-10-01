# Despliegue automatizado

## 1. Corrida del flujo

El flujo de github actions permite construir y publicar automaticamente la imagen de docker
cuando se realiza un cambio en la rama main.

Corrida de flujo:

https://github.com/suarezpenaseguidavid-netizen/despliegue-aplicaciones-docker-sergio/actions/runs/36879628310

La ejecucion corresponde al commit:

511e288 docs: documentar pruebas del despliegue

## 2. Etiqueta de la imagen publicada

La imagen se publica en github container registry (GHCR)

Repositorio de la imagen:

ghcr.io/suarezpenaseguidavid-netizen/despliegue-aplicaciones-docker-sergio

La etiqueta asociada al commit es: 

sha-511e288

Por lo tanto la imagen puede identificarse como:

ghcr.io/suarezpenaseguidavid-netizen/despliegue-aplicaciones-docker-sergio:sha-511e288

La etiqueta sha- permie relacionar la imagen con el commit que origino la construccion .

## 3. Como continuaria la cadena hasta el servidor

El proceso completo del despliegue automatizado continuaria de la siguiente manera:

1. Un cambio revisado y aprobado llega a la rama main.
2. GitHub Actions inicia un runner limpio.
3. El runner descarga el código, construye la imagen y la publica en GHCR.
4. Si el trabajo construir-y-publicar termina correctamente, el trabajo desplegar puede continuar.
5. El trabajo desplegar utilizaría SSH para conectarse al servidor.
6. En el servidor se ejecutaría docker compose pull para descargar la imagen publicada.
7. Después se ejecutaría docker compose up -d para recrear los contenedores necesarios.
8. El servidor quedaría ejecutando la nueva versión de la aplicación.

En este curso el despliegue contra el servidor compartido del aula no se ejecuta. Por eso el trabajo de despliegue queda preparado y documentado, pero no se realiza la conexión SSH a un servidor real.

## 4. Secretos necesarios

Para realizar una conexión real al servidor serían necesarios los siguientes secretos
de GitHub Actions:

SERVIDOR_SSH_KEY
SERVIDOR_HOST
SERVIDOR_USUARIO

Estos valores deben almacenarse en:

Settings → Secrets and variables → Actions

No deben escribirse directamente dentro del repositorio ni dentro del archivo YAML.

SERVIDOR_SSH_KEY contiene la clave privada utilizada para la conexión SSH.
SERVIDOR_HOST identifica el servidor al que se realizará la conexión.
SERVIDOR_USUARIO identifica el usuario utilizado para conectarse al servidor.

## 5. Reversión de un despliegue

Las imágenes se publican utilizando etiquetas asociadas al commit, por ejemplo:

sha-511e288

Si una versión nueva presentara un problema, se podría volver a utilizar una
etiqueta anterior que corresponda a una versión conocida.

En el servidor se cambiaría la referencia de la imagen en el archivo Compose hacia la
etiqueta anterior y posteriormente se ejecutaría:

docker compose pull
docker compose up -d

De esta forma se podría volver a desplegar la versión anterior sin reconstruir la
imagen desde cero.

## 6. Diferencia frente a un despliegue manual

En un despliegue manual una persona construye y publica la imagen desde su propio equipo

En el despliegue automatizado, GitHub Actions utiliza un runner limpio para 
construir la imagen y deja registrada la relación entre la imagen y el commit que la originó.

Esto permite tener una mayor trazabilidad del proceso y facilita identificar qué versión de la aplicación corresponde a cada imagen publicada.
