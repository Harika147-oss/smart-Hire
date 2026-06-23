import streamlit as st

st.set_page_config(layout="wide")

st.markdown("""
<style>

.main {
    background:#f5f7fb;
}

.card{
    background:white;
    padding:20px;
    border-radius:18px;
    box-shadow:0 2px 10px rgba(0,0,0,0.08);
    text-align:center;
}

.big-card{
    background:white;
    padding:30px;
    border-radius:20px;
    box-shadow:0 2px 10px rgba(0,0,0,0.08);
}

.metric{
    font-size:42px;
    font-weight:bold;
}

.title{
    text-align:center;
    font-size:50px;
    font-weight:bold;
}

.subtitle{
    text-align:center;
    color:gray;
    font-size:22px;
}

.job-box{
    background:white;
    padding:20px;
    border-radius:15px;
    margin-bottom:10px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="big-card">
<div class="title">Welcome to SmartHire 👋</div>
<div class="subtitle">
Your AI Powered Career Guidance Platform
</div>
</div>
""", unsafe_allow_html=True)

st.write("")

col1,col2,col3,col4,col5 = st.columns(5)

with col1:
    st.markdown("""
    <div class="card">
    <h3>Resume Score</h3>
    <div class="metric">85%</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
    <h3>Job Match</h3>
    <div class="metric">90%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
    <h3>Tests Taken</h3>
    <div class="metric">8</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="card">
    <h3>Assignments</h3>
    <div class="metric">12</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class="card">
    <h3>Highest Score</h3>
    <div class="metric">95%</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

left,right = st.columns([1,3])

with left:
    st.markdown("""
    <div class="card">
    <h2>Recommended Domain</h2>
    <h1>ML Engineer</h1>
    <p>📈 High Growth</p>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.empty()

st.write("")

st.markdown("""
<div class="big-card">
<h2>💼 Recommended Jobs</h2>
</div>
""", unsafe_allow_html=True)

jobs = [
    ("Machine Learning Engineer","90%","Bangalore"),
    ("AI Engineer","85%","Bangalore"),
    ("Data Scientist","80%","Hyderabad"),
    ("Python Developer","75%","Remote")
]

for job,score,loc in jobs:
    st.markdown(f"""
    <div class="job-box">
    <b>{job}</b>
    <span style="float:right">{score}</span><br>
    📍 {loc}
    </div>
    """, unsafe_allow_html=True)