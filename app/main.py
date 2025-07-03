import streamlit as st

st.set_page_config(page_title="Privacy Risk Analyzer", layout="centered")

st.title("🔐 Privacy Risk Analyzer")
st.write("Paste text below to detect and mask sensitive personal information.")

user_input = st.text_area("Enter your text here:", height=200)

if st.button("Analyze"):
    st.write("✅ Analysis complete.")
    st.write("This is just a placeholder. PII detection will go here.")
