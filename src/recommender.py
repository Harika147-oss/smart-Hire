import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
def recommend_jobs(resume_text):
    jobs = pd.read_csv("data/raw/jobs.csv")
    documents = list(
        jobs["skills"] + " " + jobs["description"]
    )
    documents.append(resume_text)
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(documents)
    similarity = cosine_similarity(
        vectors[-1],
        vectors[:-1]
    )
    jobs["match_score"] = similarity[0] * 100
    return jobs.sort_values(
        "match_score",
        ascending=False
    ).head(5)