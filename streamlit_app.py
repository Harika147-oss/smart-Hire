import streamlit as st

st.set_page_config(
    page_title="SmartHire",
    page_icon="💼",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>

.stApp{
    background:#f4f6fb;
}

[data-testid="stSidebar"]{
    background:#08152f;
}

[data-testid="stSidebar"] *{
    color:white;
}

.big-title{
    font-size:38px;
    font-weight:bold;
}

.card{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0px 2px 8px rgba(0,0,0,0.1);
    text-align:center;
}

.job-card{
    background:white;
    padding:20px;
    border-radius:15px;
    margin-bottom:12px;
    box-shadow:0px 2px 8px rgba(0,0,0,0.1);
}

.welcome{
    background:white;
    padding:25px;
    border-radius:20px;
    box-shadow:0px 2px 8px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

# ---------------- Sidebar ----------------
st.sidebar.title("💼 SmartHire")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Resume Analyzer",
        "Jobs",
        "Learning Resources",
        "Achievements",
        "Exams",
        "Results",
        "Notifications",
        "Profile",
        "Settings"
    ]
)

# ---------------- Dashboard ----------------
if menu == "Dashboard":

    st.markdown("""
    <div class='welcome'>
        <div class='big-title'>
        Welcome to SmartHire 👋
        </div>
        <br>
        Your AI Powered Career Guidance Platform
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    c1,c2,c3,c4,c5 = st.columns(5)

    with c1:
        st.markdown("""
        <div class='card'>
        <h4>Resume Score</h4>
        <h1>85%</h1>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class='card'>
        <h4>Job Match</h4>
        <h1>90%</h1>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class='card'>
        <h4>Tests Taken</h4>
        <h1>8</h1>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class='card'>
        <h4>Assignments</h4>
        <h1>12</h1>
        </div>
        """, unsafe_allow_html=True)

    with c5:
        st.markdown("""
        <div class='card'>
        <h4>Highest Score</h4>
        <h1>95%</h1>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.subheader("🎯 Recommended Domain")
    st.success("Machine Learning Engineer")

    st.write("")
    st.subheader("💼 Recommended Jobs")

    jobs = [
        ("Machine Learning Engineer","90%"),
        ("AI Engineer","85%"),
        ("Data Scientist","80%"),
        ("Python Developer","75%")
    ]

    for job,score in jobs:
        st.markdown(f"""
        <div class='job-card'>
            <b>{job}</b>
            <span style='float:right'>{score}</span>
        </div>
        """, unsafe_allow_html=True)

# ---------------- Resume Analyzer ----------------
elif menu == "Resume Analyzer":

    st.title("📄 Resume Analyzer")

    file = st.file_uploader(
        "Upload Resume PDF",
        type=["pdf"]
    )

    if file:
        st.success("Resume Uploaded Successfully")
        st.write("Skills Detected:")
        st.write("Python, SQL, Machine Learning")

# ---------------- Jobs ----------------
elif menu == "Jobs":

    st.title("💼 Jobs")

    st.info("Machine Learning Engineer")
    st.info("Data Scientist")
    st.info("Python Developer")

# ---------------- Learning ----------------
elif menu == "Learning Resources":

    st.title("📚 Learning Resources")

    st.write("Python")
    st.write("SQL")
    st.write("Machine Learning")

# ---------------- Achievements ----------------
elif menu == "Achievements":

    st.title("🏆 Achievements")

    st.success("Python Certificate")
    st.success("Machine Learning Internship")

# ---------------- Exams ----------------
elif menu == "Exams":

    st.title("📝 Exams")

    st.button("Python Test")
    st.button("SQL Test")

# ---------------- Results ----------------
elif menu == "Results":

    st.title("📊 Results")

    st.table({
        "Exam":["Python","SQL"],
        "Score":["90%","88%"]
    })

# ---------------- Notifications ----------------
elif menu == "Notifications":

    st.title("🔔 Notifications")

    st.info("New internship available")

# ---------------- Profile ----------------
elif menu == "Profile":

    st.title("👤 Profile")

    st.text_input("Name")
    st.text_input("Email")

# ---------------- Settings ----------------
elif menu == "Settings":

    st.title("⚙ Settings")

    theme = st.selectbox(
        "Theme",
        ["Light","Dark"]
    )

    st.write("Selected:", theme)