# ================= IMPORTS =================
import re
import PyPDF2
import docx2txt
import nltk
from nltk.corpus import stopwords
from sentence_transformers import SentenceTransformer, util

nltk.download("stopwords")

# ================= CONFIG =================
class Config:
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    SKILL_WEIGHT = 0.4
    STRENGTH_WEIGHT = 0.3
    SEMANTIC_WEIGHT = 0.3


# ================= TEXT CLEANER =================
class TextCleaner:
    stop_words = set(stopwords.words("english"))

    @staticmethod
    def clean(text):
        text = re.sub(r"[^a-zA-Z ]", " ", text)
        text = text.lower()
        words = text.split()
        words = [w for w in words if w not in TextCleaner.stop_words]
        return " ".join(words)


# ================= RESUME PARSER =================
class ResumeParser:

    @staticmethod
    def extract_text(file_path):
        if file_path.endswith(".pdf"):
            text = ""
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text
            return text

        elif file_path.endswith(".docx"):
            return docx2txt.process(file_path)

        else:
            raise ValueError("Unsupported file format")


# ================= SKILL ONTOLOGY =================
SKILL_ONTOLOGY = {
    "core": ["machine learning", "statistics", "data analysis"],
    "tools": ["python", "pandas", "numpy", "scikit-learn"],
    "advanced": ["deep learning", "transformers", "nlp"]
}


# ================= SKILL ANALYZER =================
class SkillAnalyzer:

    @staticmethod
    def extract_skills(text):
        found = []
        for level, skills in SKILL_ONTOLOGY.items():
            for skill in skills:
                if skill in text:
                    found.append(skill)
        return list(set(found))

    @staticmethod
    def skill_depth(text):
        score = 0
        for level, skills in SKILL_ONTOLOGY.items():
            for skill in skills:
                if skill in text:
                    if level == "core":
                        score += 1
                    elif level == "tools":
                        score += 2
                    elif level == "advanced":
                        score += 3
        return score / 10

    @staticmethod
    def skill_coverage(resume_skills, jd_skills):
        if not jd_skills:
            return 0
        matched = set(resume_skills).intersection(set(jd_skills))
        return len(matched) / len(jd_skills)


# ================= RESUME STRENGTH =================
class ResumeStrength:

    ACTION_VERBS = [
        "developed", "built", "designed", "implemented",
        "optimized", "analyzed", "created", "improved",
        "engineered", "deployed"
    ]

    @staticmethod
    def calculate(text):
        numbers = re.findall(r'\d+%|\d+', text)
        verbs = sum([1 for verb in ResumeStrength.ACTION_VERBS if verb in text.lower()])
        score = len(numbers) * 2 + verbs
        return min(score, 20) / 20


# ================= SEMANTIC MATCHER =================
class SemanticMatcher:

    def __init__(self):
        self.model = SentenceTransformer(Config.EMBEDDING_MODEL)

    def similarity(self, resume_text, jd_text):
        embeddings = self.model.encode([resume_text, jd_text])
        return float(util.cos_sim(embeddings[0], embeddings[1])[0][0])


# ================= MAIN ENGINE =================
class ResumeAnalyzer:

    def __init__(self):
        self.matcher = SemanticMatcher()

    def analyze(self, resume_path, job_description):

        raw_text = ResumeParser.extract_text(resume_path)
        cleaned_resume = TextCleaner.clean(raw_text)
        cleaned_jd = TextCleaner.clean(job_description)

        resume_skills = SkillAnalyzer.extract_skills(cleaned_resume)
        jd_skills = SkillAnalyzer.extract_skills(cleaned_jd)

        missing_skills = list(set(jd_skills) - set(resume_skills))

        skill_depth = SkillAnalyzer.skill_depth(cleaned_resume)
        coverage = SkillAnalyzer.skill_coverage(resume_skills, jd_skills)
        strength = ResumeStrength.calculate(raw_text)
        semantic_score = self.matcher.similarity(cleaned_resume, cleaned_jd)

        ats_score = (
            Config.SKILL_WEIGHT * skill_depth +
            Config.STRENGTH_WEIGHT * strength +
            Config.SEMANTIC_WEIGHT * semantic_score
        ) * 100

        return {
            "ATS Score": round(ats_score, 2),
            "Semantic Score": round(semantic_score, 3),
            "Skill Coverage": round(coverage * 100, 2),
            "Skill Depth": round(skill_depth, 2),
            "Resume Strength": round(strength * 100, 2),
            "Missing Skills": missing_skills,
            "Extracted Skills": resume_skills
        }