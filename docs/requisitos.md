# Requisitos de infraestructura

| Código | Requisito de infraestructura | Criterio de aceptación |
|---|---|---|
| RI-01 | Los tres servicios se ejecutan en contenedores Docker independientes. | `docker compose ps` muestra los tres servicios en estado `Up`. |
| RI-02 | Solo el proxy inverso está expuesto al exterior. | El servicio de base de datos no tiene una sección `ports` y no responde directamente desde el host. |
| RI-03 | Los datos de la base de datos persisten después de reiniciar los contenedores. | Después de ejecutar `docker compose down` y `docker compose up -d`, la información almacenada continúa disponible. |
| RI-04 | La solución puede operar con 4 GB de memoria RAM. | Con los tres servicios funcionando, `docker stats` permite verificar que el consumo de memoria se mantiene dentro de la capacidad establecida. |
| RI-05 | La configuración sensible no está escrita directamente en el código. | Las credenciales se proporcionan mediante variables de entorno y el archivo `.env` no está versionado en Git. |
| RI-06 | Los contenedores pueden comunicarse mediante una red Docker. | `docker network ls` muestra la red utilizada por los servicios y los contenedores pueden comunicarse mediante sus nombres de servicio. |
| RI-07 | Los puertos necesarios para la solución están disponibles. | `ss -tulpn` permite comprobar que los puertos requeridos no están siendo utilizados por otro servicio. |
| RI-08 | El equipo dispone de almacenamiento suficiente para la solución. | `df -h` muestra que existe espacio disponible suficiente para las imágenes, contenedores y datos persistentes. |
| RI-09 | Los servicios pueden iniciarse mediante Docker Compose. | El comando `docker compose up -d` inicia correctamente los tres servicios sin errores. |
| RI-10 | Los servicios pueden detenerse de forma controlada. | El comando `docker compose down` detiene y elimina los contenedores sin errores. |
| RI-11 | El estado de los servicios puede ser verificado. | `docker compose ps` permite comprobar si cada uno de los servicios está ejecutándose correctamente. |
| RI-12 | La solución debe contar con conectividad de red entre los servicios que lo requieran. | Se verifica desde los contenedores que los servicios necesarios pueden resolver y alcanzar el nombre del servicio correspondiente dentro de la red Docker. |
