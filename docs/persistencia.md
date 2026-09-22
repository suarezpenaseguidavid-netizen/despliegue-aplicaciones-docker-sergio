# Evidencia de Persistencia y Volúmenes (Semana 3)

## Configuración de Infraestructura

- **Volumen Administrado:** `pgdata-app`
- **Punto de Montaje en Contenedor:** `/var/lib/postgresql/data`
- **Red de Docker (Bridge):** `app-net`
- **Contenedores Interconectados:** `api-service` (API FastAPI) y `db-app` (PostgreSQL 16)

## Verificación de Persistencia y Tolerancia a Fallos
1. Se creó el volumen independiente `pgdata-app` y la red de aislamiento `app-net`.
2. Se desplegó el contenedor de la base de datos `db-app` asociando el volumen persistente.
3. Se realizó la prueba de destrucción del contenedor activo mediante el comando `docker rm -f db-app`.
4. Se re-desplegó el servicio de base de datos vinculando el mismo volumen `pgdata-app` y la red `app-net`.
5. **Resultado Exitoso:** La llamada a `curl http://localhost:8000/db-test` respondió correctamente indicando la continuidad del servicio y la preservación de los datos.
