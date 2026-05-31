from fastapi import FastAPI
import json

from app.matcher import improved_match
from app.ai import ai_optimize_resume
from app.crud import save_resume

app = FastAPI(title="AI Job Agent")


# ------------------------
# Home endpoint
# ------------------------
@app.get("/")
def home():
    return {"message": "AI Job Agent is running"}


# ------------------------
# ATS Match endpoint
# ------------------------
@app.post("/match")
def match(resume: str, job_description: str):
    score, matched, missing = improved_match(resume, job_description)

    return {
        "match_score": score,
        "matched_skills": matched,
        "missing_skills": missing
    }


# ------------------------
# AI Resume Optimization + Save to DB
# ------------------------
@app.post("/ai-optimize")
def ai_optimize(resume: str, job_description: str):
    result = ai_optimize_resume(resume, job_description)

    try:
        parsed = json.loads(result)

        record_id = save_resume(
            resume=resume,
            job_description=job_description,
            match_score=parsed.get("ats_score_estimate", None),
            ai_resume=parsed.get("rewritten_resume", None)
        )

        parsed["saved_id"] = record_id
        return parsed

    except Exception:
        return {
            "error": "AI returned invalid JSON",
            "raw_output": result
        }
