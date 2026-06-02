import os
import json
import sqlite3
import io
from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pypdf import PdfReader

app = FastAPI()

# Enable CORS bridging so your local Firefox frontend can talk to Uvicorn smoothly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize client (will fallback safely if using local mock development)
client = OpenAI()

def find_matching_companies(user_skills):
    try:
        conn = sqlite3.connect("jobs.db")
        cursor = conn.cursor()
        cursor.execute("SELECT company_name, job_title, required_skills, location, apply_link FROM companies")
        all_jobs = cursor.fetchall()
        conn.close()
    except Exception as db_err:
        print(f"Database error: {str(db_err)}")
        return []

    matched_companies = []
    for company, title, req_skills, location, link in all_jobs:
        skill_list = [s.strip().lower() for s in req_skills.split(",")]
        overlap = [skill for skill in skill_list if skill in [u.lower() for u in user_skills]]
        if overlap:
            matched_companies.append({
                "company": company,
                "title": title,
                "location": location,
                "matched_skills": overlap,
                "link": link
            })
    return matched_companies

@app.get("/")
def home():
    return {"message": "AI Job Agent API is running successfully!"}

@app.post("/api/match")
async def match(
    job_description: str = Form(...), 
    file: UploadFile = File(...)
):
    try:
        print(f"--- SMART AI REQUEST RECEIVED FOR: {file.filename} ---")
        
        # Read file bytes
        file_bytes = await file.read()
        resume_text = ""

        # Safe PDF structural text extraction
        if file.filename.lower().endswith('.pdf'):
            print("Processing PDF file extraction...")
            pdf_file = io.BytesIO(file_bytes)
            reader = PdfReader(pdf_file)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    resume_text += text + "\n"
        else:
            # Fallback text decoder
            resume_text = file_bytes.decode("utf-8", errors="ignore")

        if not resume_text.strip():
            print("Extraction failed: Resume text is completely empty.")
            raise HTTPException(status_code=400, detail="Could not extract text from the uploaded file.")

        # --- CHOOSE YOUR MODE HERE ---
        # Switch USE_MOCK to False once you add funds ($5) to your OpenAI Billing account to run real queries.
        USE_MOCK = True 

        if USE_MOCK:
            print("Bypassing OpenAI API - Generating Free Local Mock Dashboard Data...")
            smart_analysis = {
                "score": 85,
                "matched": ["Python", "FastAPI", "Linux", "Networking", "Cybersecurity", "HTML", "CSS", "JavaScript"],
                "missing": ["Docker", "AWS Cloud", "CI/CD Pipelines"],
                "job_requirements": ["Backend API Development", "System Infrastructure", "Network Security Protocols"],
                "improvements": [
                    "Incorporate your Shield Up Cybersecurity job simulation metrics.",
                    "Detail your live FastAPI project (Cyberconnect-form) directly in your work history description.",
                    "Highlight your experience handling Fedora system text environment configurations."
                ],
                "explanation": "Your technical core in networking, script automations, and frontend layout structures matches the technical stack extremely well. Introducing cloud provisioning skills will unlock premium target roles."
            }
        else:
            print("Sending data to OpenAI GPT-4o-mini...")
            system_prompt = (
                "You are an expert ATS optimizer and elite career coach. "
                "Analyze the user's resume against the job description. "
                "Provide a logical match score (0 to 100), extract matched skills, and extract missing skills. "
                "Identify what the job demands most, and give highly specific, actionable advice. "
                "You MUST respond ONLY with a valid JSON object using this exact structure:\n"
                "{\n"
                '  "score": 75,\n'
                '  "matched": ["Python", "Linux"],\n'
                '  "missing": ["Docker", "Kubernetes"],\n'
                '  "job_requirements": ["Backend development", "Container orchestration"],\n'
                '  "improvements": ["Add metrics", "Build a portfolio project"],\n'
                '  "explanation": "A concise overview."\n'
                "}"
            )

            user_prompt = f"RESUME TEXT:\n{resume_text}\n\nJOB DESCRIPTION:\n{job_description}"

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3
            )
            smart_analysis = json.loads(response.choices[0].message.content)
            print("AI analysis completed successfully via OpenAI.")

        # Cross-reference the database for matching opportunities
        skills_found = smart_analysis.get("matched", [])
        recommendations = find_matching_companies(skills_found)
        smart_analysis["hiring_companies"] = recommendations

        return smart_analysis

    except Exception as e:
        print(f"CRITICAL ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
