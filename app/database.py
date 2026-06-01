from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime

# SQLite database (file will be created automatically)
DATABASE_URL = "sqlite:///./job_agent.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


# ------------------------
# Table structure
# ------------------------
class ResumeRecord(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String, nullable=True)

    resume = Column(Text, nullable=False)
    job_description = Column(Text, nullable=True)

    match_score = Column(Float, nullable=True)
    ai_resume = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)


# Create tables
Base.metadata.create_all(bind=engine)
