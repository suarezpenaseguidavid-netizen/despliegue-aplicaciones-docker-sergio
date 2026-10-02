# Despliegue de aplicaciones Docker

Proyecto del curso Despliegue de aplicaciones en contenedores Docker, orientado a la construcción, configuración, ejecución y publicación automatizada de una aplicación mediante contenedores.

## 1. ¿Qué hace esta solución?

La solución está compuesta por tres servicios:

- Nginx: recibe las solicitudes HTTP y funciona como proxy inverso.
- API: desarrollada con Python, FastAPI y Uvicorn.
- PostgreSQL: almacena los datos de la aplicación.

Los servicios se ejecutan mediante Docker Compose y se comunican a través de una red interna llamada backend.

La arquitectura permite que únicamente Nginx tenga un puerto publicado hacia el equipo anfitrión. La API y PostgreSQL permanecen disponibles mediante la red interna de Docker.

La base de datos utiliza un volumen Docker para conservar la información cuando los contenedores son detenidos y posteriormente levantados nuevamente.

## 2. Requisitos

Para ejecutar el proyecto se necesita:

- Equipo personal con conexión a Internet.
- Docker.
- Docker Compose.
- Git.
- Acceso al repositorio de GitHub.

## Instalación del motor Docker

Las instrucciones específicas para instalar y verificar Docker en los tres sistemas operativos se encuentran documentadas en:

`docs/entorno.md`

El documento incluye la ruta de instalación utilizada durante el desarrollo y la verificación mediante:

- docker --version
- docker compose version
- docker run --rm hello-world

La solución puede utilizarse en:

- Windows.
- Linux.
- macOS.

En Windows y macOS se puede utilizar Docker Desktop. En Linux se puede utilizar Docker Engine siguiendo la documentación correspondiente al sistema operativo.

## 4. Clonar el repositorio

Clonar el proyecto:

```bash
git clone https://github.com/suarezpenaseguidavid-netizen/despliegue-aplicaciones-docker-sergio.git
```

Ingresar al directorio:

```bash
cd despliegue-aplicaciones-docker-sergio
```

## 5. Configurar las variables de entorno

El proyecto utiliza la variable DB_PASSWORD para establecer la contraseña de PostgreSQL.

Crear el archivo .env a partir de la plantilla:

```bash
cp .env.example .env
```

Editar el archivo:

```bash
nano .env
```

Definir una contraseña: `DB_PASSWORD=una_contrasena_segura`

El archivo .env está incluido en .gitignore para evitar publicar la contraseña en el repositorio.

## 6. Construir y levantar la solución

Para construir la imagen de la API y levantar todos los servicios:

```bash
docker compose up -d --build
```

Docker Compose realizará las siguientes acciones:

1. Construirá la imagen de la API.
2. Creará la red backend.
3. Creará el volumen db_data.
4. Iniciará PostgreSQL.
5. Esperará a que PostgreSQL esté saludable.
6. Iniciará la API.
7. Iniciará Nginx.

## 7. Verificar los servicios

Consultar el estado de los contenedores:

```bash
docker compose ps
```

Se deben encontrar los siguientes servicios:

- api-service
- db-app
- nginx

El servicio db-app debe aparecer como healthy.

## 8. Probar la API

La API dispone de un endpoint de salud:

```bash
curl http://localhost/health
```

Respuesta esperada:

```JSON
{
	"status": "ok",
	"message": "API running correctly"
}
```

También existe un endpoint para comprobar la conexión con PostgreSQL:

```bash
curl http://localhost/db-test
```

Si la conexión funciona correctamente, la respuesta contiene información sobre la versión de PostgreSQL.

## 9. Detener la solución

Para detener y eliminar los contenedores:

```bash
docker compose down
```

El volumen db_data se conserva.

Para eliminar también los volúmenes:

```bash
docker compose down -v
```

**Advertencia**: docker compose down -v elimina el volumen de PostgreSQL y, por tanto, los datos almacenados en él.

## 10. Publicación automática de la imagen

El repositorio utiliza GitHub Actions para automatizar la construcción y publicación de la imagen Docker.

El flujo se encuentra en: `.github/workflows/publicar-imagen.yml`

Cuando se realiza un push a la rama main, GitHub Actions ejecuta el proceso automatizado.

paso a paso del proceso principal es:

1. Código
2. GitHub Actions
3. Construcción de la imagen
4. Publicación en GitHub Container Registry
5. Imagen Docker etiquetada

La imagen se publica en **GitHub Container Registry (GHCR)**.

Nombre de la imagen: `ghcr.io/suarezpenaseguidavid-netizen/despliegue-aplicaciones-docker-sergio`

El flujo genera etiquetas que permiten identificar las versiones de las imágenes, incluyendo etiquetas asociadas al commit mediante SHA.

La documentación específica del proceso de despliegue automatizado se encuentra en:

`docs/despliegue-automatizado.md`

## 11. Documentación adicional

| **Documento** | **Descripcion** |
| docs/entorno.md | Instalación y configuración del entorno Docker |
| docs/requisitos.md | Requisitos de infraestructura |
| docs/manual-tecnico.md | Arquitectura y operación técnica |
| docs/pruebas.md | Pruebas realizadas a la solución |
| docs/despliegue-automatizado.md | Automatización de publicación y despliegue |

## 12. Repositorio

Repositorio del proyecto: `https://github.com/suarezpenaseguidavid-netizen/despliegue-aplicaciones-docker-sergio`

