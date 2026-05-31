from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.orm import declarative_base, sessionmaker

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
    resume = Column(Text)
    job_description = Column(Text)
    match_score = Column(Float)
    ai_resume = Column(Text)


# Create tables
Base.metadata.create_all(bind=engine)
