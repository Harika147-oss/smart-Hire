def skill_gap(resume_text):

    resume = resume_text.lower()

    required = [
        "python",
        "java",
        "machine learning",
        "artificial intelligence",
        "deep learning",
        "sql",
        "flask",
        "pandas",
        "numpy",
        "aws"
    ]

    have = []
    missing = []

    for skill in required:
        if skill in resume:
            have.append(skill)
        else:
            missing.append(skill)

    return have, missing