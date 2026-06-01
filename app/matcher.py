import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

STOPWORDS = [
    "the", "and", "with", "for", "a", "an", "to", "of", "in", "on", "is", "are",
    "looking", "role", "job", "experience", "candidate", "you", "our", "team", "work"
]

def clean_and_tokenize(text: str):
    """ Cleans text, preserves technical symbols, and returns a sanitized string """
    if not text:
        return ""
    text = text.lower()
    # Safely preserve characters for languages/tools like C++, C#, .NET
    text = re.sub(r"[^a-z0-9+.# ]", " ", text)
    return text

def improved_match(resume: str, job_description: str):
    cleaned_resume = clean_and_tokenize(resume)
    cleaned_job = clean_and_tokenize(job_description)

    if not cleaned_resume or not cleaned_job:
        return 0.0, [], []

    # 1. MATHEMATICAL SIMILARITY (The real core score)
    # TfidfVectorizer analyzes phrase density and automatically extracts weights.
    # ngram_range=(1, 3) allows it to read "linux", "cyber security", and "cloud systems administration"
    vectorizer = TfidfVectorizer(stop_words=STOPWORDS, ngram_range=(1, 3))
    
    try:
        tfidf_matrix = vectorizer.fit_transform([cleaned_job, cleaned_resume])
        # Calculate mathematical vector closeness between the two texts
        similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        raw_score = float(similarity_matrix[0][0]) * 100
    except ValueError:
        # Fallback if no meaningful words are matched
        raw_score = 0.0

    # 2. DYNAMIC SKILL EXTRACTION (Extracting the real skills listed in the job)
    # We use a single-word extraction pass to show matched vs missing lists cleanly
    word_vectorizer = TfidfVectorizer(stop_words=STOPWORDS, ngram_range=(1, 1))
    
    try:
        word_matrix = word_vectorizer.fit_transform([cleaned_job, cleaned_resume])
        feature_names = word_vectorizer.get_feature_names_out()
        
        job_vector = word_matrix.toarray()[0]
        resume_vector = word_matrix.toarray()[1]

        matched_skills = []
        missing_skills = []

        for idx, word in enumerate(feature_names):
            # If the word has weight inside the job description...
            if job_vector[idx] > 0:
                # ...and it's present in the resume
                if resume_vector[idx] > 0:
                    matched_skills.append(word)
                else:
                    # If the job values it highly (above average frequency), mark as critical missing
                    if job_vector[idx] > 0.15: 
                        missing_skills.append(word)

    except ValueError:
        matched_skills, missing_skills = [], []

    # Format output precisely for your system architecture
    return round(raw_score, 1), matched_skills, missing_skills
