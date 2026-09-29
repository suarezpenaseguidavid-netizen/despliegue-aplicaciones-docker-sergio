# Plataforma completa (Semana 4 - RA2)

## Servicios
| Servicio | Imagen | Puerto | Exposición |
|---|---|---|---|
| nginx | nginx:alpine | 80 | Público (único punto de entrada) |
| api-service | build local (FastAPI, Python 3.12) | 8000 | Solo red interna `backend` |
| db-app | postgres:18-alpine | 5432 | Solo red interna `backend` |

## Red y volumen
- Red: `backend` (bridge)
- Volumen: `db_data` montado en `/var/lib/postgresql`

## Arranque
    docker compose up -d --build

## Flujo
Cliente -> Nginx (:80) -> api-service (:8000) -> db-app (:5432)

## Verificación
- `curl http://localhost/health` responde a través de Nginx.
- `curl http://localhost/db-test` confirma la conexión a PostgreSQL 18.
- `curl http://localhost:8000/` falla: la API no está expuesta.
- Persistencia comprobada: la fila insertada en la tabla `prueba` sobrevive a `docker compose down` y `up`.
