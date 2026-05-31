from app.database import SessionLocal, ResumeRecord


def save_resume(resume, job_description, match_score=None, ai_resume=None):
    db = SessionLocal()

    record = ResumeRecord(
        resume=resume,
        job_description=job_description,
        match_score=match_score,
        ai_resume=ai_resume
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    db.close()

    return record.id
