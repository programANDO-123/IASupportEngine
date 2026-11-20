
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.requests import Request

from app.api.routes import router

app = FastAPI(
    title="AI Support Engine",
    description="API para clasificar solicitudes de soporte",
    version="1.0.0",
)
app.include_router(router)


@app.exception_handler(RequestValidationError)
async def invalid_request(_request: Request, _error: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Envíe un message de 1 a 2000 caracteres y un mode traditional o generative."
        },
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
