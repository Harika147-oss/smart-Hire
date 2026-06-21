def find_skill_gap(resume_text, job_skills):

    resume_text = resume_text.lower()

    skills = [
        "python",
        "java",
        "c",
        "sql",
        "excel",
        "aws",
        "machine learning",
        "artificial intelligence",
        "data analysis",
        "jupyter notebook",
        "matlab"
    ]

    candidate_skills = []

    for skill in skills:
        if skill in resume_text:
            candidate_skills.append(skill)

    missing_skills = []

    for skill in job_skills:
        if skill.lower() not in candidate_skills:
            missing_skills.append(skill)

    return missing_skills