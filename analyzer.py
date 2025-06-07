import google.generativeai as genai

def configure_gemini(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")

def analyze_resume(model, resume_text, job_description):
    prompt = f"""
    You are an experienced HR like (Application tracking system, ATS) with Technical Experience in the field of any one job role from Data Science, Data Analyst, DevOPS, Machine Learning Engineer, Prompt Engineer, AI Engineer, Full Stack Web Development, Big Data Engineering, Marketing Analyst, Human Resource Manager, Software Developer your task is to review the provided resume.
    Please share your professional evaluation on whether the candidate's profile aligns with the role.ALso mention Skills he already have and suggest some skills to imorve his resume , alos suggest some course he might take to improve the skills.Highlight the strengths and weaknesses.
    give ATS score with the current resume he has.
    
    Resume:
    {resume_text}

    Job Description:
    {job_description}

    Output:
    1. ATS Match Score (0-100)
    2. Key Strengths
    3. Weaknesses
    4. Suggestions for Improvement
    """

    response = model.generate_content(prompt)
    return response.text
