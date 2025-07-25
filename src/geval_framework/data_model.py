from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class GEvalResponse(BaseModel):
    """G-Eval Response Model"""

    metric_score: float
    metric_explanation: str
    detailed_results: Optional[List[Dict[str, Any]]] = None


class MetricResult(BaseModel):
    score: int = Field(ge=1, le=5, description="Evaluation score between 1 and 3")
    reasoning: str = Field(description="Brief explanation of the evaluation in Korean")
