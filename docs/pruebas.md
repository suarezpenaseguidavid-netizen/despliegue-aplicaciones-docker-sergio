# Pruebas de despliegue

## 1. Levantamiento de la solucion

Se verifico que la solucion puede levantarse correctamente mediante Docker compose

Comandos utilizados:

```bash
docker compose up -d
```

Psterior mente se comprobo los estados de los servicios:

```bash
docker compose ps
```

Resultado:

* api-service: Up
* db-app: Up (healthy)
* nginx: Up

El servicio Nginx se encuentra publicado en el puerto 8080 del host mientras que la API
y la base de datos no tienen puertos publicados directamente hacia el host.

### RESULTADO: APROBADO

## 2. Funcionamiento de la red interna 

Se comprobo que la API puede resolver el nombre del servisio de base de datos dentro de la red
interna de Docker.

Comandos utilizados:

```bash
docker compose exec api-service python -c "import socket; print(socket.gethostbyname('db-app'))"
```

Resultado obtenido: 172.20.0.2

La direccion obtenida corresponde a una IP privada de la red de docker. Esto demuestra que el
servicio **api-service** puede resolver el nombre **db-app** mediante el DNS interno proporcionado
por docker compose.

### RESULTADO: APROBADO

## 3. Persistencia de los datos

Se verifico inicialmente la existencia de un registro en la tabla **prueba**

Comandos utilizados:

```bash
docker compose exec db-app psql -U appuser -d appdb -c "SELECT * FROM prueba;"
```

Resultado antes del reinicio:

| id | texto |
| --- | --- |
| 1 | persiste |

Posteriormente se detuvieron y eliminaron los contenedores:

```bash
docker compose down
```

y se levantaron nuevamente:

```bash
docker compose up -d
```

Después del reinicio, el servicio **db-app** volvió a aparecer como **healthy**

Se ejecutó nuevamente la consulta:

```bash
docker compose exec db-app psql -U appuser -d appdb -c "SELECT * FROM prueba;"
```

Resultado después del reinicio:

| id | texto |
| --- | --- |
| 1 | persiste |

El registro permanecio despues de detener y volver a levantar los contenedores, demostrando que
los datos de PostgreSQL se mantienen mediante el volumen configurado.

### RESULTADO: APROBADO

## 4. Aislamiento de la base de datos

Se verificó que el puerto 5432 de PostgreSQL no está publicado hacia el host.

Comando utilizado:

```bash
docker inspect despliegue-aplicaciones-docker-sergio-db-app-1 --format '{{json .NetworkSettings.Ports}}'
```

Resultado: {"5432/tcp":null}

Esto indica que el puerto **5432** esta disponible dentro del contenedor, pero no existe un mapeo 
del puerto hacia el host.

También se realizó una prueba de acceso desde el host:

```bash
curl --max-time 3 http://localhost:5432 || echo "correcto: la BD no responde desde el host"
```

Resultado:

curl: (52) Empty reply from server
correcto: la BD no responde desde el host

La base de datos no está publicada directamente hacia el host y permanece accesible mediante
la red interna de Docker.

### RESULTADO: APROBADO

## Conclusion

Las pruebas realizadas verificaron:

1. El levantamiento correcto de la solución.
2. La comunicación entre la API y la base de datos mediante la red interna de Docker.
3. La persistencia de los datos después de detener y volver a levantar los contenedores.
4. El aislamiento de la base de datos respecto al host.

**Estado general de las pruebas: APROBADO**
