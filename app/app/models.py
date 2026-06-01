from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from app.database import Base

class MatchHistory(Base):
    __tablename__ = "match_history"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    score = Column(Float, nullable=False)
    matched_skills = Column(String, nullable=False)  # Stored as comma-separated string
    missing_skills = Column(String, nullable=False)  # Stored as comma-separated string
