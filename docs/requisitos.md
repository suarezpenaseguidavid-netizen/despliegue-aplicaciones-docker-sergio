# Requisitos de infraestructura

## Matriz de requisitos

| Código | Requisito de infraestructura | Criterio de aceptación |
|---|---|---|
| RI-01 | Los tres servicios se ejecutan en contenedores Docker independientes. | `docker compose ps` muestra los tres servicios en estado `Up`. |
| RI-02 | Solo el proxy inverso está expuesto al exterior. | El servicio de base de datos no tiene sección `ports` y no responde directamente desde el host. |
| RI-03 | Los datos de la base de datos persisten después de reiniciar los contenedores. | Después de ejecutar `docker compose down` y `docker compose up -d`, los datos continúan disponibles. |
| RI-04 | La solución puede operar con 4 GB de memoria RAM. | `docker stats` permite comprobar el consumo de memoria de los tres servicios. |
| RI-05 | La configuración sensible no está escrita directamente en el código. | Las credenciales se proporcionan mediante variables de entorno y `.env` no está versionado. |

## Servicios de la solución

| Componente | Imagen base | Puerto interno | Requisito clave |
|---|---|---:|---|
| Proxy inverso | `nginx:1.30-alpine` | 80 | Enrutar las peticiones a la API |
| API backend | `python:3.14-slim` o `node:24-alpine` | 8000 | Conexión a la base de datos |
| Base de datos | `postgres:18-alpine` | 5432 | Almacenamiento persistente mediante volumen |

## Sistemas operativos

| RI-OS-01 | La solución debe poder ejecutarse en Windows mediante Docker. | Al ejecutar `docker compose up -d`, los tres servicios se inician correctamente en Windows. |
| RI-OS-02 | La solución debe poder ejecutarse en Linux mediante Docker. | Al ejecutar `docker compose up -d`, los tres servicios se inician correctamente en Linux. |
| RI-OS-03 | La solución debe poder ejecutarse en macOS mediante Docker. | Al ejecutar `docker compose up -d`, los tres servicios se inician correctamente en macOS. |
