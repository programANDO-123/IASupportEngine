# AI Support Engine

API para el análisis y clasificación de solicitudes de soporte técnico mediante un motor tradicional basado en reglas y un motor de inteligencia artificial generativa.

## Objetivo

Desarrollar una solución que permita analizar solicitudes de soporte, identificar su categoría y prioridad, y generar una respuesta apropiada.

## Tecnologías

- Python 3.11
- FastAPI
- Uvicorn
- Docker
- Docker Compose

## Requisitos previos

- Docker Desktop instalado y en ejecución.
- Git para administrar el código fuente.

No es necesario instalar Python ni las dependencias del proyecto localmente para ejecutar la aplicación mediante Docker.

## Estructura del proyecto

```text
ai-support-engine/
├── app/
│   ├── __init__.py
│   └── main.py
├── tests/
├── docs/
├── requirements.txt
├── Dockerfile
├── compose.yaml
├── .dockerignore
├── .gitignore
└── README.md
```

## Instalación y ejecución

1. Clonar el repositorio.
2. Entrar a la carpeta del proyecto.
3. Construir e iniciar el contenedor:

```bash
docker compose up -d --build
```

## Acceso a la API

- Página principal: http://localhost:8000
- Estado de salud: http://localhost:8000/health
- Documentación interactiva: http://localhost:8000/docs

## Verificación

Consultar el estado del contenedor:

```bash
docker compose ps
```

Consultar la versión de Python utilizada dentro del contenedor:

```bash
docker compose exec api python --version
```

## Detener la aplicación

```bash
docker compose down
```

## Estado del proyecto

La estructura inicial y el entorno de ejecución con Docker están preparados. La implementación de los motores de clasificación, el endpoint de análisis y sus pruebas se desarrollarán en las siguientes etapas.