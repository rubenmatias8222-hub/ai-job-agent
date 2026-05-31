import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ai_optimize_resume(resume: str, job_description: str):
    prompt = f"""
You are an expert ATS resume writer.

Your task:
Rewrite the resume to better match the job description.

Rules:
- Do NOT invent fake experience
- Improve wording to match job requirements
- Add missing skills ONLY if they are implied or reasonable
- Make it ATS-friendly and professional
- Keep it realistic and honest

Return STRICT JSON ONLY in this format:

{{
  "rewritten_resume": "...",
  "added_skills": ["..."],
  "improvements": ["..."],
  "ats_score_estimate": number
}}

Resume:
{resume}

Job Description:
{job_description}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a strict JSON resume optimization engine."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
