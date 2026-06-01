from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.matcher import improved_match  # IMPORTANT

app = FastAPI(title="AI Job Agent")

# ------------------------
# FRONTEND
# ------------------------
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

# ------------------------
# REQUEST MODEL
# ------------------------
class MatchRequest(BaseModel):
    resume: str
    job_description: str

# ------------------------
# API ROUTE
# ------------------------
@app.post("/api/match")
def match(data: MatchRequest):
    score, matched, missing = improved_match(data.resume, data.job_description)
    return {
        "score": score,
        "matched": matched,
        "missing": missing
    }
