import streamlit as st
from resume_engine import ResumeAnalyzer

st.set_page_config(page_title="Resume Analyzer", layout="wide")

uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])

# 🔥 Make Job Description Box Bigger
job_description = st.text_area(
    "Paste Job Description",
    height=350   # 👈 increase height (you can set 400 or 500 if needed)
)

if uploaded_file and job_description:

    with open("temp_resume.pdf", "wb") as f:
        f.write(uploaded_file.read())

    analyzer = ResumeAnalyzer()
    result = analyzer.analyze("temp_resume.pdf", job_description)

    st.markdown("## 📊 Resume Evaluation Dashboard")

    st.metric("ATS Score", f"{result['ATS Score']}%")
    st.metric("Semantic Score", result["Semantic Score"])
    st.metric("Skill Coverage", f"{result['Skill Coverage']}%")
    st.metric("Skill Depth", result["Skill Depth"])
    st.metric("Resume Strength", f"{result['Resume Strength']}%")

    st.subheader("🔍 Missing Skills")
    st.write(result["Missing Skills"])

    st.subheader("📌 Detected Technical Skills")
    st.write(result["Extracted Skills"])

else:
    st.info("Upload resume and paste job description to begin.")