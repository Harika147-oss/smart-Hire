import streamlit as st

st.title("📊 Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Resumes Uploaded", "25")

with col2:
    st.metric("Jobs Applied", "12")

with col3:
    st.metric("Courses Completed", "8")