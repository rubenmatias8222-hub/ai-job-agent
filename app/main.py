from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import os

from app.database import engine, Base, get_db
from app.models import MatchHistory
from app.schemas import MatchRequest, MatchHistoryResponse
from app.matcher import improved_match

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Job Agent Pro")

@app.post("/api/match")
def match(data: MatchRequest, db: Session = Depends(get_db)):
    try:
        # Destructure the 4 fields from our upgraded intelligence module
        score, matched, missing, ai_feedback = improved_match(data.resume, data.job_description)

        matched_str = ", ".join(matched) if matched else "None"
        missing_str = ", ".join(missing) if missing else "None"

        # Commit directly into database tables
        db_record = MatchHistory(
            score=score,
            matched_skills=matched_str,
            missing_skills=missing_str,
            ai_explanation=ai_feedback  # SAVING THE NEW LAYER HERE
        )
        db.add(db_record)
        db.commit()
        db.refresh(db_record)

        return {
            "score": db_record.score,
            "matched": matched,
            "missing": missing,
            "explanation": ai_feedback  # TRANSMITTING TO FRONTEND UI
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/history", response_model=list[MatchHistoryResponse])
def get_history(db: Session = Depends(get_db)):
    return db.query(MatchHistory).order_by(MatchHistory.id.desc()).all()

if os.path.exists("frontend"):
    app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
