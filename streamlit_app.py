import streamlit as st
import pdfplumber
import pandas as pd
import os

st.set_page_config(
    page_title="SmartHire",
    page_icon="💼",
    layout="centered"
)

st.title("💼 SmartHire - Resume Job Matching Portal")

st.write("Upload your resume and get job recommendations")

uploaded_file = st.file_uploader(
    "Upload Your Resume (PDF)",
    type=["pdf"]
)

if uploaded_file:

    text = ""

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

    st.success("Resume Uploaded Successfully!")

    st.subheader("📄 Resume Text")
    st.write(text)


    # Simple skill detection
    skills = [
        "Python",
        "Java",
        "C",
        "SQL",
        "Machine Learning",
        "Data Science",
        "HTML",
        "CSS",
        "JavaScript"
    ]

    found_skills = []

    for skill in skills:
        if skill.lower() in text.lower():
            found_skills.append(skill)


    st.subheader("✅ Detected Skills")

    if found_skills:
        st.write(", ".join(found_skills))
    else:
        st.write("No skills detected")


    st.subheader("🎯 Predicted Job Domain")

    if "python" in text.lower() or "machine learning" in text.lower():
        category = "AI / Machine Learning"
    elif "html" in text.lower() or "javascript" in text.lower():
        category = "Web Development"
    else:
        category = "Software Development"

    st.write(category)


    st.subheader("📊 Skill Gap Report")

    missing = []

    for skill in skills:
        if skill not in found_skills:
            missing.append(skill)

    if missing:
        st.write(
            "Improve these skills: "
            + ", ".join(missing)
        )
    else:
        st.write("Great! Your skills match well.")


    st.subheader("💼 Recommended Jobs")

    jobs = {
        "Python Developer Intern":
        "Python, SQL, Git",

        "Machine Learning Intern":
        "Python, ML, Data Science",

        "Web Developer Intern":
        "HTML, CSS, JavaScript"
    }


    for job, req in jobs.items():
        st.write("### " + job)
        st.write("Required Skills:", req)

        score = len(
            set(found_skills) &
            set(req.split(", "))
        )

        st.write(
            "Match Score:",
            str(score * 25) + "%"
        )
