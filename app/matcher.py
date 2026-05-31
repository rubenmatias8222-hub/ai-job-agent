import re

STOPWORDS = {
    "the", "and", "with", "for", "a", "an", "to", "of", "in", "on",
    "we", "are", "is", "looking", "role", "job", "experience", "candidate"
}

# Weighted skills (IMPORTANT PART)
SKILL_WEIGHTS = {
    "linux": 2.0,
    "cybersecurity": 2.5,
    "siem": 3.0,
    "networking": 2.0,
    "firewall": 2.5,
    "python": 2.0,
    "aws": 2.5,
    "docker": 1.5,
    "kubernetes": 1.5
}

def clean_text(text: str):
    text = text.lower()
    text = re.sub(r"[^a-z0-9+.# ]", " ", text)
    return text.split()

def improved_match(resume: str, job: str):
    resume_words = clean_text(resume)
    job_words = clean_text(job)

    resume_set = set(resume_words)

    total_score = 0
    max_score = 0

    matched = []
    missing = []

    for skill in SKILL_WEIGHTS:
        weight = SKILL_WEIGHTS[skill]
        max_score += weight

        if skill in resume_set and skill in job_words:
            total_score += weight
            matched.append(skill)
        elif skill in job_words:
            missing.append(skill)

    score = (total_score / max_score) * 100 if max_score > 0 else 0

    return round(score, 2), matched, missing
