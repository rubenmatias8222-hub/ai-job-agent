import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

STOPWORDS = [
    "the", "and", "with", "for", "a", "an", "to", "of", "in", "on", "is", "are",
    "looking", "role", "job", "experience", "candidate", "you", "our", "team", "work"
]

def clean_and_tokenize(text: str):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"[^a-z0-9+.# ]", " ", text)
    return text

def generate_ai_explanation(score: float, matched: list, missing: list) -> str:
    """ Real-Time AI Critic Layer: Generates context-aware strategic career feedback """
    if score == 0:
        return "The system could not establish a connection between your resume and the target job description. Ensure you have copied valid text into both fields."
    
    # Contextual analysis variables
    missing_count = len(missing)
    matched_count = len(matched)
    
    # 1. Executive Summary Component
    if score >= 80:
        summary = f"Excellent alignment! Your application profile demonstrates strong technical authority for this position, matching {matched_count} key environmental parameters."
    elif score >= 50:
        summary = f"Moderate structural fit detected. Your resume establishes a reliable foundational baseline, but lacks core specific specializations emphasized by the employer."
    else:
        summary = f"Critical alignment gap. The system detected high-density keywords within the job requirements that are completely omitted or unaddressed within your current resume profile."

    # 2. Strategic Action Insight Component
    if missing:
        critical_targets = missing[:3] # Focus on the top 3 high-priority missing terms
        action_plan = f"To bypass corporate screening boundaries, you must systematically inject these critical terms into your professional summary or experiential bullets: {', '.join(critical_targets)}."
    else:
        action_plan = "Your technical keyword layout is optimal. Focus now on refining your quantified metric achievements (e.g., 'Reduced system vulnerabilities by 20%') to stand out during human review."

    # 3. Final Combined Intelligence Output
    full_analysis = f"{summary} {action_plan} Current Match Confidence: {score}%."
    return full_analysis


def improved_match(resume: str, job_description: str):
    cleaned_resume = clean_and_tokenize(resume)
    cleaned_job = clean_and_tokenize(job_description)

    if not cleaned_resume or not cleaned_job:
        return 0.0, [], [], "Incomplete input fields."

    # Mathematical Vector Core
    vectorizer = TfidfVectorizer(stop_words=STOPWORDS, ngram_range=(1, 3))
    try:
        tfidf_matrix = vectorizer.fit_transform([cleaned_job, cleaned_resume])
        similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        raw_score = float(similarity_matrix[0][0]) * 100
    except ValueError:
        raw_score = 0.0

    # Skill Array Extraction Passing
    word_vectorizer = TfidfVectorizer(stop_words=STOPWORDS, ngram_range=(1, 1))
    try:
        word_matrix = word_vectorizer.fit_transform([cleaned_job, cleaned_resume])
        feature_names = word_vectorizer.get_feature_names_out()
        job_vector = word_matrix.toarray()[0]
        resume_vector = word_matrix.toarray()[1]

        matched_skills = []
        missing_skills = []

        for idx, word in enumerate(feature_names):
            if job_vector[idx] > 0:
                if resume_vector[idx] > 0:
                    matched_skills.append(word)
                else:
                    if job_vector[idx] > 0.12: # Configured sensitivity threshold
                        missing_skills.append(word)
    except ValueError:
        matched_skills, missing_skills = [], []

    # COMPUTE THE NEW AI EXPLANATION LAYER
    ai_feedback = generate_ai_explanation(round(raw_score, 1), matched_skills, missing_skills)

    return round(raw_score, 1), matched_skills, missing_skills, ai_feedback
