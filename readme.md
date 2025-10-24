# Proyecto de conexion con New Relic - 01
    Probando conexion con python 3.11

## Crear entorno virtual
  python3.11 -m venv env_proyecto

## -- Clear cache python
  ```bash
  $ find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
  ```
# Levantar el Dockerfile NewRelic - imagen Base
  ```bash
  docker build -f Dockerfile_newrelic -t python_newrelic:latest .
  ```
# Construir la aplicación :
  ```bash
  docker build -t my_python_api .
  ```
# Ejecutar la instancia de la imagen
  ```bash
  docker run \
  -e NEW_RELIC_LICENSE_KEY=<personal_token> \
  -e NEW_RELIC_APP_NAME="Python Application" \
  -e FASTAPI_ENV=develop \
  -p 8000:8000 -it --rm --name fastapi_newrelic my_python_api:latest
  ```

-----------------------------------------
# Instrucciones de Uso
  1. Configuración:
      ```bash
      cp .env.example .env
      # Edita .env con tus configuraciones de NewRelic
      ```
  2. Instalación:
      `pip install -r requirements.txt`

  3. Ejecución local:
      ```bash
      cd src
      python main.py
      # O con uvicorn directamente:
      uvicorn main:app --reload --host 0.0.0.0 --port 8000
      ```
  4. Construcción Docker:
      ```bash
      docker build -t fastapi-newrelic-demo .
      docker run -p 8000:8000 --env-file .env fastapi-newrelic-demo
      ```
  5. Documentación Swagger:
      - Swagger UI: http://localhost:8000/docs
      - ReDoc: http://localhost:8000/redoc
      - OpenAPI JSON: http://localhost:8000/openapi.json

  6. Verificar la configuración:
      ```bash
        cd src
        python check_newrelic.py
      ```
  7. Ejecutar la aplicación manualmente:
      ```bash
      python main.py
      ```
