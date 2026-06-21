from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def match_resume(resume, job):

    documents = [
        resume,
        job
    ]

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(documents)

    score = cosine_similarity(
        vectors[0],
        vectors[1]
    )

    percentage = round(score[0][0] * 100, 2)

    return percentage