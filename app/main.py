from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import os

from app.database import engine, Base, get_db
from app.models import MatchHistory
from app.schemas import MatchRequest, MatchHistoryResponse
from app.matcher import improved_match

# Initialize database tables on app startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Job Agent")

# ----------------------------------------------------
# 1. PROCESS & SAVE MATCH
# ----------------------------------------------------
@app.post("/api/match")
def match(data: MatchRequest, db: Session = Depends(get_db)):
    try:
        score, matched, missing = improved_match(data.resume, data.job_description)

        # Convert list format into simple database-friendly text format
        matched_str = ", ".join(matched) if matched else "None"
        missing_str = ", ".join(missing) if missing else "None"

        # Save record directly into history
        db_record = MatchHistory(
            score=round(float(score), 1),
            matched_skills=matched_str,
            missing_skills=missing_str
        )
        db.add(db_record)
        db.commit()
        db.refresh(db_record)

        return {
            "score": db_record.score,
            "matched": matched,
            "missing": missing
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----------------------------------------------------
# 2. FETCH HISTORICAL RUNS
# ----------------------------------------------------
@app.get("/api/history", response_model=list[MatchHistoryResponse])
def get_history(db: Session = Depends(get_db)):
    # Pull history logs, newest first
    history = db.query(MatchHistory).order_by(MatchHistory.id.desc()).all()
    return history

# ----------------------------------------------------
# SERVE FRONTEND STATIC ASSETS
# ----------------------------------------------------
if os.path.exists("frontend"):
    app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
