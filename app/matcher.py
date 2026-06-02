import re

STOPWORDS = {
    "the", "and", "with", "for", "a", "an", "to", "of", "in", "on",
    "we", "are", "is", "looking", "role", "job", "experience", "candidate"
}

SKILL_WEIGHTS = {
    "linux": 2.0,
    "cybersecurity": 2.5,
    "siem": 3.0,
    "networking": 2.0,
    "firewall": 2.5,
    "python": 2.0,
    "aws": 2.5,
    "docker": 1.5,
    "kubernetes": 1.5,
    "cloud": 2.0,
    "computing": 1.5,
    "sql": 2.0,
    "git": 1.0
}

def clean_text(text: str):
    if not text:
        return []

    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    words = text.split()

    return [w for w in words if w not in STOPWORDS]


def improved_match(resume: str, job: str):
    resume_words = set(clean_text(resume))
    job_words = set(clean_text(job))

    matched_skills = []
    missing_skills = []

    total_weight = 0.0
    matched_weight = 0.0

    for skill, weight in SKILL_WEIGHTS.items():
        total_weight += weight

        if skill in resume_words and skill in job_words:
            matched_skills.append(skill)
            matched_weight += weight
        elif skill in job_words:
            missing_skills.append(skill)

    if total_weight == 0:
        return 0.0, [], []

    score = (matched_weight / total_weight) * 100

    return round(score, 2), matched_skills, missing_skills
