
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
def train_classifier():

    data = pd.read_csv(
        "data/processed/resume_categories.csv"
    )


    vectorizer = TfidfVectorizer()

    X = vectorizer.fit_transform(
        data["resume_text"]
    )

    y = data["category"]


    model = LogisticRegression()

    model.fit(X,y)


    return model, vectorizer



def predict_category(text):

    model, vectorizer = train_classifier()

    x = vectorizer.transform([text])

    result = model.predict(x)

    return result[0]