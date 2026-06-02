from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.matcher import improved_match
# 1. Initialize the FastAPI app instance
app = FastAPI()

# 2. Define your request model
class MatchRequest(BaseModel):
    resume: str
    job_description: str

# 3. Root GET Route (Separated cleanly)
from fastapi.responses import FileResponse

@app.get("/")
def home():
    return FileResponse("app/index.html")

# 4. Match POST Route (Fixed syntax and indentation)
@app.post("/api/match")
def match(data: MatchRequest):
    try:
        print("--- API REQUEST RECEIVED ---")
        resume_text = data.resume or ""
        job_text = data.job_description or ""

        print("RESUME:", resume_text[:200])
        print("JOB:", job_text[:200])

        # Assuming improved_match is imported or defined elsewhere in your project
        score, matched, missing = improved_match(resume_text, job_text)

        print("DEBUG OUTPUT -> Score:", score,
              "| Matched:", matched,
              "| Missing:", missing)

        return {
            "score": float(score),
            "matched": matched,
            "missing": missing,
            "explanation": f"Match analysis completed with {len(matched)} matched skills and {len(missing)} missing skills."
        }

    except Exception as e:
        print(f"ERROR DURING MATCHING: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal matching error: {str(e)}"
        )
