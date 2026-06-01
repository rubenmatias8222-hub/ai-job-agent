from pydantic import BaseModel
from datetime import datetime
from typing import List

class MatchRequest(BaseModel):
    resume: str
    job_description: str

class MatchHistoryResponse(BaseModel):
    id: int
    timestamp: datetime
    score: float
    matched_skills: str
    missing_skills: str
    ai_explanation: str  # NEW LAYER FIELD

    class Config:
        from_attributes = True
