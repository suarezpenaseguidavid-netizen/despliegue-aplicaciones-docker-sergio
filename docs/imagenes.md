# IMAGENES DE DOCKER UTILIZADAS

Durante la práctica se utilizaron las siguientes imágenes Docker

## Imagen

- **PostgreSQL**

## Etiqueta

- postgres:18-alpine

## Tamaño

- 121MB

## Proposito

Servidor de base de datos PostgreSQL 18 utilizado para crear el contenedor db-app

## Imagen

- **Nginx**

## Etiqueta

- nginx:1.30-alpine

## Tamaño

- 29.4MB

## Proposito

Servidor web utilizado para levantar el contenedor web y realizar una prueba mediante el puerto 8080.

# USO DE LAS IMAGENES

**postgres:18-alpine**

Imagen utilizada para ejecutar PostgreSQL 18 en el contenedor db-app. Se configuró una base de datos llamada appdb y un volumen Docker para practicar la persistencia de datos.

**nginx:1.30-alpine**

Imagen utilizada para ejecutar Nginx en el contenedor web. Se publicó el puerto 80 del contenedor mediante el puerto 8080 del equipo anfitrión y se verificó su funcionamiento mediante curl http://localhost:8080.
