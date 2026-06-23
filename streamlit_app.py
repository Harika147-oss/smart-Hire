import streamlit as st

st.set_page_config(
    page_title="SmartHire",
    page_icon="💼",
    layout="wide"
)

st.markdown("""
<style>

[data-testid="stSidebar"]{
    background-color:#0b1736;
}

[data-testid="stSidebar"] *{
    color:white;
}

.main{
    background-color:#f4f6f9;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
# 💼 SmartHire

## Welcome to SmartHire 👋

### Your AI Powered Career Guidance Platform

Use the sidebar to access all modules.

### Available Features

- Dashboard
- Resume Analyzer
- Job Recommendations
- Career Roadmap
- Learning Resources
- Resume Score
- Assignments
- Exams
- Results
- Achievements
- Notifications
- Settings

""")