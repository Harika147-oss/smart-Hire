import streamlit as st
import pdfplumber

# ----------------------------
# PAGE CONFIG
# ----------------------------

st.set_page_config(
    page_title="SmartHire",
    page_icon="💼",
    layout="wide"
)

# ----------------------------
# SIDEBAR MENU
# ----------------------------

page = st.sidebar.selectbox(
    "Navigation",
    [
        "Home",
        "Resume Analyzer",
        "Jobs",
        "Learning Resources",
        "Profile"
    ]
)

# ----------------------------
# HOME PAGE
# ----------------------------

if page == "Home":

    st.title("💼 SmartHire")

    st.markdown("""
    ### Welcome to SmartHire

    SmartHire is an AI-powered Resume Job Matching Portal.

    Features:
    - Resume Upload
    - Skill Detection
    - Job Domain Prediction
    - Skill Gap Analysis
    - Job Recommendations
    - Learning Resources
    """)

# ----------------------------
# RESUME ANALYZER PAGE
# ----------------------------

elif page == "Resume Analyzer":

    st.title("📄 Resume Analyzer")

    uploaded_file = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"]
    )

    if uploaded_file:

        text = ""

        with pdfplumber.open(uploaded_file) as pdf:

            for page_pdf in pdf.pages:

                page_text = page_pdf.extract_text()

                if page_text:
                    text += page_text

        st.success("Resume Uploaded Successfully!")

        st.subheader("📄 Resume Text")

        st.write(text)

        # ----------------------------
        # SKILL DETECTION
        # ----------------------------

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

            st.success(", ".join(found_skills))

        else:

            st.warning("No skills detected")

        # ----------------------------
        # JOB DOMAIN PREDICTION
        # ----------------------------

        st.subheader("🎯 Predicted Job Domain")

        if (
            "python" in text.lower()
            or "machine learning" in text.lower()
            or "data science" in text.lower()
        ):

            category = "AI / Machine Learning"

        elif (
            "html" in text.lower()
            or "css" in text.lower()
            or "javascript" in text.lower()
        ):

            category = "Web Development"

        elif (
            "sql" in text.lower()
        ):

            category = "Data Analytics"

        else:

            category = "Software Development"

        st.info(category)

        # ----------------------------
        # SKILL GAP REPORT
        # ----------------------------

        st.subheader("📊 Skill Gap Report")

        missing = []

        for skill in skills:

            if skill not in found_skills:

                missing.append(skill)

        if missing:

            st.error(
                "Improve these skills:\n\n"
                + ", ".join(missing)
            )

        else:

            st.success(
                "Great! Your skills match well."
            )

        # ----------------------------
        # JOB RECOMMENDATIONS
        # ----------------------------

        st.subheader("💼 Recommended Jobs")

        jobs = {
            "Python Developer Intern":
            ["Python", "SQL"],

            "Machine Learning Intern":
            ["Python", "Machine Learning", "Data Science"],

            "Web Developer Intern":
            ["HTML", "CSS", "JavaScript"],

            "Data Analyst Intern":
            ["SQL", "Python", "Data Science"]
        }

        for job, req_skills in jobs.items():

            score = len(
                set(found_skills)
                &
                set(req_skills)
            )

            match_percentage = (
                score / len(req_skills)
            ) * 100

            st.markdown(f"### {job}")

            st.write(
                "Required Skills:",
                ", ".join(req_skills)
            )

            st.progress(
                int(match_percentage)
            )

            st.write(
                f"Match Score: {match_percentage:.2f}%"
            )

# ----------------------------
# JOBS PAGE
# ----------------------------

elif page == "Jobs":

    st.title("💼 Available Jobs")

    st.markdown("### Python Developer Intern")

    st.write("""
    Skills:
    - Python
    - SQL
    - Git
    """)

    st.markdown("### Machine Learning Intern")

    st.write("""
    Skills:
    - Python
    - Machine Learning
    - Data Science
    """)

    st.markdown("### Web Developer Intern")

    st.write("""
    Skills:
    - HTML
    - CSS
    - JavaScript
    """)

# ----------------------------
# LEARNING PAGE
# ----------------------------

elif page == "Learning Resources":

    st.title("📚 Learning Resources")

    st.write(
        "Python: https://www.w3schools.com/python/"
    )

    st.write(
        "SQL: https://www.w3schools.com/sql/"
    )

    st.write(
        "Machine Learning: https://www.coursera.org"
    )

    st.write(
        "HTML/CSS: https://www.w3schools.com"
    )

# ----------------------------
# PROFILE PAGE
# ----------------------------

elif page == "Profile":

    st.title("👤 Candidate Profile")

    st.write("Name: Candidate")

    st.write("Status: Active")

    st.write(
        "Use Resume Analyzer to upload resume."
    )