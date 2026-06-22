import streamlit as st

st.title("⚙️ Settings")

theme = st.selectbox(
    "Theme",
    ["Light", "Dark"]
)

st.write("Selected Theme:", theme)