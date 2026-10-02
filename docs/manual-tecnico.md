# Manual tecnico

## 1. Descripción de la solución

La solución implementa una aplicación distribuida mediante contenedores Docker.
La arquitectura está compuesta por tres servicios:

- **Nginx:** servidor web y proxy inverso.
- **API:** aplicación desarrollada con Python, FastAPI y Uvicorn.
- **PostgreSQL:** sistema gestor de base de datos.

Los servicios se comunican mediante una red interna de Docker denominada `backend`.
La única entrada publicada hacia el equipo anfitrión es Nginx. La API y PostgreSQL permanecen 
disponibles únicamente dentro de la red interna de Docker.

## 2. Servicios y puertos

| Servicios | Imagen / Tecnologia | Puerto interno | Puerto publico |
| **Nginx** | `nginx:alpine` | 80 | 80 |
| **api-service** | Python 3.12 + FastAPI | 8000 | No publico |
| **db-app** | `Postgres:18-alpine` | 5432 | No publico |


El puerto 80 es el único puerto publicado hacia el host.
La API escucha internamente en el puerto 8000, pero no tiene un mapeo ports, por lo que no se
accede directamente desde el host.

PostgreSQL utiliza el puerto interno 5432 y tampoco tiene un mapeo de puertos hacia el host.

## 4. Docker

Los tres servicios pertenecen a la red: backend
La red utiliza el controlador: bridge

Docker Compose proporciona resolución de nombres entre los servicios de la red. Por esta razón
a API puede conectarse a PostgreSQL utilizando:

DB_HOST=db-app

No es necesario utilizar una dirección IP fija para la base de datos La comunicación interna
utiliza los siguientes nombres y puertos:

nginx -> api-service:8000
api-service -> db-app:5432

## 5. Volúmenes y persistencia

La base de datos utiliza el volumen Docker: db_data

Este volumen se monta en: /var/lib/postgresql

Su finalidad es conservar los datos de PostgreSQL aunque los contenedores sean detenidos o
recreados.

El volumen se declara en `docker-compose.yml`:

volumenes:
 db_data:

La persistencia fue comprobada mediante la creación de un registro en la base de datos, seguido
de:

```bash
docker compose down
```

y posteriormente:

```bash
docker compose up -d
```

Después del reinicio, el registro continuó disponible.

## 6. Variables de entorno

La solución utiliza variables de entorno para configurar la conexión entre la API y PostgreSQL.

| Variable | Valor |
| **DB_HOST** | db_app |
| **DB_PORT** | 5432 |
| **DB_NAME** | appdb |
| **DB_USER** | appuser |
| **DB_PASSWORD** | Valor definido `.env` |

### PostgreSQL

| Variable | Valor |
| **POSTGRES_DB** | appdb |
| **POSTGRES_USER** | appuser |
| **POSTGRES_PASSWORD** | Valor definido en `.env` |

La contraseña se obtiene mediante: ${DB_PASSWORD}

El archivo .env está excluido del repositorio mediante .gitignore para evitar publicar
informacion sensible.

Se dispone de un archivo .env.example con la estructura necesaria: DB_PASSWORD=

## 7. Construcción de la imagen de la API

La API utiliza un Dockerfile de múltiples etapas.

La primera etapa instala las dependencias de Python y la segunda contiene únicamente
los elementos necesarios para ejecutar la aplicación.

La imagen utiliza: `python:3.12-slim`

La aplicación se ejecuta mediante Uvicorn: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

El contenedor ejecuta la aplicación con un usuario no root denominado: `appuser`

## 8. Endpoints de la API

La API dispone de los siguientes endpoints: **GET /health**

Permite comprobar que la API está funcionando.

Respuesta esperada:

```JSON
{
	"status": "ok",
	"message": "API running correctly"
}
```

**GET /db-test** Comprueba la conexión entre la API y PostgreSQL.
Si la conexión es correcta, devuelve información sobre la versión de PostgreSQL.

## 9. Instalación y despliegue

### 9.1 Requisitos previos

Se requiere:

- Sistema operativo Windows, Linux o macOS.
- Docker Engine o Docker Desktop según el sistema operativo.
- Docker Compose.
- Conexión a Internet.
- Git, para clonar el repositorio.

Las instrucciones específicas de instalación del motor Docker se encuentran en: `docs/entorno.md`

### 9.2 Obtener el proyecto

Clonar el repositorio:

```bash
git clone https://github.com/suarezpenaseguidavid-netizen/despliegue-aplicaciones-docker-sergio.git
```

Ingresar al proyecto:

```bash
cd despliegue-aplicaciones-docker-sergio
```

### 9.3 Configurar las variables de entorno

Crear el archivo `.env` :

```bash
cp .env.example .env
```

Editar el archivo:

```bash
nano .env
````

Definir una contraseña para PostgreSQL: DB_PASSWORD=una_contrasena_segura

Guardar los cambios.

El archivo `.env` no debe publicarse en el repositorio.

### 9.4 Construir y levantar la solución

Ejecutar:

```bash
docker compose up -d --build
```

Este comando construye la imagen de la API y levanta los tres servicios.

Comprobar el estado:

```bash
docker compose ps
```

Los servicios esperados son:

- api-service
- db-app
- nginx

PostgreSQL debe aparecer como healthy.

### 9.5 Verificar la API

Desde el equipo anfitrión se puede consultar:

```bash
curl http://localhost/health
```

También se puede comprobar la conexión con PostgreSQL mediante:

```bash
curl http://localhost/db-test
```

## 10. Comandos principales de operación

Levantar la solucion:

```bash
docker compose up -d
̣```

Levantar reconstruyendo las imágenes:

```bash
docker compose up -d --build
```

Ver el estado de los servicios:

```bash
docker compose ps
```

Ver los registros:

```bash
docker compose logs -f
```

Detener y eliminar los contenedores:

```bash
docker compose down
```

El volumen db_data se conserva.

Detener los contenedores y eliminar los volúmenes:

```bash
docker compose down -v
```

Este comando elimina también el volumen de PostgreSQL y, por tanto, sus datos persistidos.

## 11. Despliegue automatizado

El repositorio utiliza GitHub Actions para automatizar la construcción y publicación de la imagen Docker.

El flujo se ejecuta cuando se realiza un push a la rama main o cuando se publica una
etiqueta de versión compatible con el patrón configurado.

El orden  de la  automatización es:

1. Cambio en el repositorio
2. GitHub Actions
3. Construcción de la imagen
4. Publicación en GHCR
5. Etiqueta de la imagen
6. Proceso de despliegue

La imagen se publica en GitHub Container Registry (GHCR).

El nombre del registro utilizado por el proyecto es:
`ghcr.io/suarezpenaseguidavid-netizen/despliegue-aplicaciones-docker-sergio`

Las etiquetas basadas en SHA permiten identificar la imagen correspondiente al commit que la originó.

El trabajo de despliegue está condicionado a que el trabajo de construcción y publicación
termine correctamente y a que el flujo corresponda a la rama main.

Las credenciales necesarias para una conexión SSH al servidor se manejan mediante
secretos de GitHub Actions y no se almacenan directamente en el repositorio.

Los secretos contemplados por el flujo son:

`SERVIDOR_SSH_KEY`
`SERVIDOR_HOST`
`SERVIDOR_USUARIO`

En el entorno de formación utilizado para este proyecto no se realiza el despliegue sobre
un servidor compartido del aula.

## 12. Verificación y pruebas

Las pruebas realizadas se encuentran documentadas en:

`docs/pruebas.md`

Se verificaron:

1. Levantamiento correcto de los servicios.
2. Comunicación entre la API y PostgreSQL mediante la red interna.
3. Persistencia de los datos mediante el volumen Docker.
4. Aislamiento de PostgreSQL respecto al host.

El estado general de las pruebas fue: **APROBADO**

## 13. Rollback

En un escenario productivo, las imágenes deben identificarse mediante etiquetas
inmutables, por ejemplo:

`sha-<commit>`

Ante un problema con una versión desplegada, el procedimiento consiste en utilizar
nuevamente una etiqueta anterior conocida y ejecutar:

```bash
docker compose pull
docker compose up -d
```

Esto permite volver a ejecutar una versión anterior de la imagen sin reconstruirla localmente.

## 14. Archivos principales

| **Archivos** | **Funcion** |
| docker-compose.yml | Orquestación de los servicios |
| Dockerfile | Construcción de la imagen de la API |
| nginx/default.conf | Configuración del proxy inverso |
| app/main.py | Código de la API |
| requirements.txt | Dependencias Python |
| .env.example | Plantilla de variables de entorno |
| .gitignore | Exclusión de archivos sensibles |
| .github/workflows/publicar-imagen.yml | Automatización CI/CD |
| docs/entorno.md | Documentación del entorno Docker |
| docs/pruebas.md | Evidencias de pruebas |
| docs/despliegue-automatizado.md | Documentación del despliegue automatizado |

