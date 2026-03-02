# 📊 AI Resume Analyzer

An NLP-powered Resume Evaluation Dashboard built using Python and Streamlit.

This application analyzes resumes against job descriptions and provides an ATS-style evaluation using semantic similarity, skill matching, and weighted scoring.

---

## 🚀 Project Demo

https://github.com/user-attachments/assets/4ed909ba-250a-40e8-8f4d-e586abc71f67

---

## 🧠 Features

- ATS Score Calculation
- Semantic Similarity Score
- Skill Coverage Percentage
- Skill Depth Analysis
- Resume Strength Evaluation
- Missing Skill Detection
- Detected Technical Skills Display
- Clean Streamlit Dashboard

---

## 📊 Resume Evaluation Dashboard

The dashboard displays:

- ATS Score
- Semantic Score
- Skill Coverage
- Skill Depth
- Resume Strength
- Predicted Role (Placeholder)
- Missing Skills
- Detected Technical Skills

---

## 🧠 How It Works

1. Resume text is extracted from PDF or DOCX files.
2. The text is cleaned using NLP preprocessing techniques.
3. Skills are detected using a custom skill ontology.
4. Semantic similarity is calculated using the Sentence Transformers model (all-MiniLM-L6-v2).
5. The ATS score is computed using weighted scoring combining:
   40% Skill Depth,
   30% Resume Strength,
   30% Semantic Similarity.
6. Missing skills are identified by comparing resume skills with job description skills.

---

## 🛠 Tech Stack

Python  
Streamlit  
Sentence Transformers  
Scikit-learn  
NLTK  
PyPDF2  
docx2txt  

---

## 📦 Installation

Clone the repository:

git clone https://github.com/AryanDekate12/ai-resume-analyzer.git  
cd ai-resume-analyzer  

Install dependencies:

pip install -r requirements.txt  

Run the application:

python -m streamlit run app.py  

---

## 📁 Project Structure

ai-resume-analyzer/  
│  
├── app.py  
├── resume_engine.py  
├── requirements.txt  
├── README.md  
└── demo.mp4 (optional)  

---

## 👨‍💻 Author

Aryan Dekate  
B.Tech – Information Technology  
Interested in AI, NLP, and Data Science
