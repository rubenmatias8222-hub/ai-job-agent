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

    class Config:
        from_attributes = True
