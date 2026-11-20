from fastapi import APIRouter, HTTPException

from app.engines.generative import ProviderError
from app.schemas.support import AnalysisRequest, AnalysisResponse
from app.services.support import analyze

router = APIRouter(prefix="/api")


@router.post("/analyze", response_model=AnalysisResponse)
def analyze_request(request: AnalysisRequest) -> AnalysisResponse:
    try:
        return analyze(request)
    except ProviderError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from None
