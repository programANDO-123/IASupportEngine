from app.engines import generative, rules
from app.schemas.support import AnalysisRequest, AnalysisResponse


def analyze(request: AnalysisRequest) -> AnalysisResponse:
    if request.mode == "traditional":
        result = rules.classify(request.message)
    else:
        result = generative.classify(request.message)
        if result.category == "SECURITY" or rules.has_security_signal(request.message):
            result.requiresHumanReview = True
    return AnalysisResponse(**result.model_dump(), mode=request.mode)
