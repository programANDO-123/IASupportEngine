from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, StrictBool

Mode = Literal["traditional", "generative"]
Category = Literal["ACCESS", "BUG", "FEATURE", "SECURITY"]
Priority = Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]


class AnalysisRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, strict=True)

    message: str = Field(min_length=1, max_length=2000)
    mode: Mode


class AnalysisResult(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, strict=True)

    category: Category
    priority: Priority
    response: str = Field(min_length=1, max_length=1200)
    requiresHumanReview: StrictBool


class AnalysisResponse(AnalysisResult):
    mode: Mode
