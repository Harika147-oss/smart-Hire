import streamlit as st

st.set_page_config(layout="wide")

st.markdown("""
<style>
.main {
    background-color: #f2f5f9;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
}

.big-card {
    background: white;
    padding: 30px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
}

.job-box {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
}

h1,h2,h3{
    color:#0b1736;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='big-card'>
<h1>Welcome to SmartHire 👋</h1>
<h3>Your AI Powered Career Guidance Platform</h3>
</div>
""", unsafe_allow_html=True)

st.write("")

col1,col2,col3,col4,col5 = st.columns(5)

with col1:
    st.markdown("""
    <div class='card'>
    <h3>Resume Score</h3>
    <h1>85%</h1>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='card'>
    <h3>Job Match</h3>
    <h1>90%</h1>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='card'>
    <h3>Tests Taken</h3>
    <h1>8</h1>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class='card'>
    <h3>Assignments</h3>
    <h1>12</h1>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class='card'>
    <h3>Highest Score</h3>
    <h1>95%</h1>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

left,right = st.columns([1,2])

with left:
    st.markdown("""
    <div class='card'>
    <h3>Recommended Domain</h3>
    <h1>ML Engineer</h1>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class='job-box'>
    <h2>💼 Recommended Jobs</h2>

    <p>Machine Learning Engineer - 90% Match</p>
    <hr>

    <p>AI Engineer - 85% Match</p>
    <hr>

    <p>Data Scientist - 80% Match</p>
    <hr>

    <p>Python Developer - 75% Match</p>

    </div>
    """, unsafe_allow_html=True)