# Administración de Imágenes y Evidencia Multi-Etapa (Semana 3)

## Registro de Imagen Construida

| Nombre de la Imagen | Etiqueta | ID de Imagen | Tamaño Final |
| :--- | :--- | :--- | :--- |
| `api-app` | `1.0.0` | `08444ea8a666` | **55.5 MB** |
| `api-app` | `latest` | `08444ea8a666` | **55.5 MB** |

## Análisis de Infraestructura y Buenas Prácticas

1. **Optimización con Dockerfile Multi-Etapa:**
   - Se utilizó una primera etapa (`builder`) con la imagen base `python:3.14-slim` para compilar e instalar las dependencias (`fastapi` y `uvicorn`) en la ruta especificada `--prefix=/install`.
   - En la etapa final de ejecución, solo se copiaron los paquetes instalados desde `/install` hacia `/usr/local`, descartando librerías de desarrollo, cachés de `pip` y archivos temporales de compilación.
   - Resultado: La imagen se redujo a solo **55.5 MB**.

2. **Seguridad y Menos Privilegios:**
   - Se creó el usuario del sistema `appuser` con UID `1001`.
   - La aplicación se ejecuta bajo la directiva `USER appuser`, evitando la ejecución como `root` dentro del contenedor.

3. **Operaciones de Ciclo de Vida Ejecutadas:**
   - **Etiquetado:** Se versionó la imagen `1.0.0` y se asoció el tag `latest`.
   - **Inspección de capas:** Se utilizó `docker history api-app:1.0.0` para verificar la adición de archivos por capa.
   - **Diagnóstico de espacio:** Se verificó el almacenamiento utilizado con `docker system df`.
