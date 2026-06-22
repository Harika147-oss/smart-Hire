def predict_domain(text):

    text = text.lower()

    if "machine learning" in text or "tensorflow" in text:
        return "Machine Learning Engineer"

    elif "data science" in text or "pandas" in text:
        return "Data Scientist"

    elif "html" in text or "css" in text or "javascript" in text:
        return "Web Developer"

    elif "sql" in text or "power bi" in text:
        return "Data Analyst"

    else:
        return "Python Developer"