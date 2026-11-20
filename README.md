# AI Support Engine

API de soporte técnico con FastAPI. El motor tradicional clasifica con reglas y devuelve una respuesta predeterminada. El motor generativo usa Qwen2.5 Instruct en un servidor local de llama.cpp para clasificar y redactar una respuesta contextualizada.

## Ejecutar

1. Descarga [llama.cpp b12498](https://github.com/ggml-org/llama.cpp/releases/tag/b12498) para tu sistema. En Windows x64 puedes usar el ZIP `llama-b12498-bin-win-cpu-x64.zip`.
2. Descarga el modelo oficial [Qwen2.5 1.5B Instruct Q4_K_M](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/blob/main/qwen2.5-1.5b-instruct-q4_k_m.gguf). Desde donde extrajiste llama.cpp, inicia el servidor. Ajusta la ruta al archivo GGUF:

```powershell
.\llama-server.exe -m "C:\ruta\qwen2.5-1.5b-instruct-q4_k_m.gguf" --alias qwen2.5-1.5b --host 127.0.0.1 --port 8081 -c 8192 -np 1
```

3. En otra terminal, desde el repositorio y con Python 3.11 o superior, prepara e inicia la API:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

También puedes iniciar la API con `docker compose up -d --build` en Docker Desktop. Compose usa `http://host.docker.internal:8081` para el modelo en la máquina anfitriona. Si el proveedor está en otra dirección alcanzable desde el contenedor, define `LLAMA_BASE_URL` antes de ejecutar Compose. Fuera de Docker la URL por defecto es `http://127.0.0.1:8081`. `LLAMA_MODEL` cambia el alias del modelo. El motor tradicional funciona aunque el proveedor local esté apagado. La configuración local no requiere claves.

## Analizar una solicitud

Abre la [documentación interactiva](http://localhost:8000/docs) y ejecuta `POST /api/analyze`:

```json
{ "message": "No puedo iniciar sesión", "mode": "traditional" }
```

Ambos modos (`traditional` y `generative`) devuelven `category`, `priority`, `response`, `requiresHumanReview` y `mode`. Las categorías son `ACCESS`, `BUG`, `FEATURE` y `SECURITY`. Las prioridades son `LOW`, `MEDIUM`, `HIGH` y `CRITICAL`. Los posibles incidentes de seguridad se marcan para revisión humana.

Los mensajes deben tener entre 1 y 2000 caracteres después de quitar los espacios alrededor. La API responde con `422` a entradas inválidas, `502` si el proveedor devuelve una respuesta inválida o falla, `503` si no está disponible y `504` si excede el tiempo de espera. `/health` comprueba que la API esté activa.

## Comparación de los motores

Con ambos servicios en ejecución, corre desde el repositorio:

```powershell
.\.venv\Scripts\python.exe tests/comparative.py
```

Se ejecutan los 12 [casos de referencia](tests/comparative_cases.json) contra cada motor. La [tabla comparativa](evidence/RESULTADOS.md) registra categoría, prioridad, validez de formato y aciertos. El [registro HTTP](evidence/results.json) contiene las solicitudes y las respuestas completas.

## Conclusión técnica

En esta prueba con 12 solicitudes, el motor tradicional obtuvo 11 aciertos (91,67 %) y Qwen2.5 1.5B obtuvo 4 (33,33 %). Ambos cumplieron el contrato JSON en los 12 casos. Las reglas funcionaron mejor porque aplicaron criterios de prioridad consistentes y resistieron los dos intentos de manipulación. Su único error fue interpretar una mejora expresada de forma indirecta como una falla. El modelo generativo redactó respuestas contextualizadas, pero confundió categorías y prioridades. En particular, asignó prioridad `LOW` a una filtración activa cuyo mensaje pedía rebajarla, aunque conservó la revisión humana. Estos resultados corresponden a este conjunto de pruebas y a esta versión del modelo.
