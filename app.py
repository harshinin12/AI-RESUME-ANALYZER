import os
import re
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv

from utils import extract_text_from_pdf
from analyzer import configure_gemini, analyze_resume

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Streamlit page configuration
st.set_page_config(page_title="AI Resume Analyzer", layout="centered")
st.markdown("<h1 style='text-align:center;'>🤖 AI Resume Analyzer</h1>", unsafe_allow_html=True)

# File upload and input fields
uploaded_file = st.file_uploader("📄 Upload Your Resume (PDF)", type=["pdf"])
job_description = st.text_area("📝 Enter Job Description")

if st.button("Analyze"):
    if uploaded_file and job_description and api_key:
        with st.spinner("Analyzing with Gemini..."):
            try:
                model = configure_gemini(api_key)
                resume_text = extract_text_from_pdf(uploaded_file)
                result = analyze_resume(model, resume_text, job_description)

                # Extract Analysis Data
                ats_score_match = re.search(r"(?i)ATS Match Score.*?(\d+)", result)
                ats_score = int(ats_score_match.group(1)) if ats_score_match else 0

                strengths = re.search(r"(?i)Strengths\s*[:\-]*([\s\S]*?)Weaknesses", result)
                weaknesses = re.search(r"(?i)Weaknesses\s*[:\-]*([\s\S]*?)Suggestions", result)
                suggestions = re.search(r"(?i)Suggestions.*?:\s*([\s\S]*)", result)

                strengths_text = strengths.group(1).strip() if strengths else "Not Found"
                weaknesses_text = weaknesses.group(1).strip() if weaknesses else "Not Found"
                suggestions_text = suggestions.group(1).strip() if suggestions else "Not Found"

                # Extract Keywords (Example Logic)
                job_keywords = set(job_description.lower().split())
                resume_keywords = set(resume_text.lower().split())

                relevant_keywords = job_keywords.intersection(resume_keywords)
                irrelevant_keywords = resume_keywords.difference(job_keywords)

                relevant_counts = {kw: resume_text.lower().count(kw) for kw in relevant_keywords}
                irrelevant_counts = {kw: resume_text.lower().count(kw) for kw in irrelevant_keywords}

                # Display Analysis
                st.subheader("🔍 Analysis Result")
                st.markdown(f"### ✅ ATS Score: {ats_score}/100")

                # Donut Chart for ATS Score
                fig, ax = plt.subplots(figsize=(6, 6))
                ax.pie(
                    [ats_score, 100 - ats_score],
                    labels=["Matched", "Not Matched"],
                    startangle=90,
                    counterclock=False,
                    colors=["#4B9CD3", "#D3D3D3"],
                    wedgeprops=dict(width=0.3, edgecolor='w')
                )
                plt.text(0, 0, f"{ats_score}%", ha='center', va='center', fontsize=24)
                ax.set_aspect('equal')
                st.pyplot(fig)

                

                # Display Extracted Information
                st.success("✅ Key Strengths")
                st.markdown(strengths_text)

                st.error("⚠️ Weaknesses")
                st.markdown(weaknesses_text)

                st.info("📈 Suggestions for Improvement")
                st.markdown(suggestions_text)

            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")
    else:
        st.warning("Please upload a resume and enter a job description.")

# Footer
st.markdown("---")
st.markdown("<footer style='text-align:center;'>Developed by N. HARSHINI</footer>", unsafe_allow_html=True)
