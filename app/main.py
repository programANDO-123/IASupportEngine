
from fastapi import FastAPI

app = FastAPI(
    title="AI Support Engine",
    description="API para clasificar solicitudes de soporte",
    version="1.0.0",
)


@app.get("/")
def home():
    return {
        "message": "AI Support Engine funcionando correctamente",
        "status": "ok",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
