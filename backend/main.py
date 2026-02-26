from fastapi import FastAPI, UploadFile, File
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from utils.text_processing import extract_text_from_pdf, clean_text
from io import BytesIO
import numpy as np

# -----------------------------
# Initialize FastAPI
# -----------------------------
app = FastAPI()

# Load embedding model once at startup
model = SentenceTransformer("all-MiniLM-L6-v2")


@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = ""
):
    try:
        # -----------------------------
        # Read and process resume PDF
        # -----------------------------
        contents = await resume.read()
        pdf_file = BytesIO(contents)

        resume_text = extract_text_from_pdf(pdf_file)
        resume_text = clean_text(resume_text)
        job_description = clean_text(job_description)

        if not resume_text:
            return {"error": "Could not extract text from PDF."}

        # -----------------------------
        # Semantic Similarity
        # -----------------------------
        embeddings = model.encode([resume_text, job_description])

        similarity_score = cosine_similarity(
            [embeddings[0]],
            [embeddings[1]]
        )[0][0]

        similarity_percent = round(float(similarity_score) * 100, 2)

        # -----------------------------
        # Skill Matching
        # -----------------------------
        skill_keywords = [
            "python", "machine learning", "tensorflow", "pytorch",
            "llm", "rag", "vector database", "langchain",
            "langgraph", "api", "docker", "kubernetes",
            "fastapi", "aws", "azure", "gcp", "eks",
            "ci/cd", "gitlab", "mlops"
        ]

        jd_skills = [skill for skill in skill_keywords if skill in job_description]
        resume_skills = [skill for skill in skill_keywords if skill in resume_text]

        matched_skills = list(set(jd_skills).intersection(set(resume_skills)))
        missing_skills = list(set(jd_skills) - set(resume_skills))

        skill_match_percent = 0
        if len(jd_skills) > 0:
            skill_match_percent = round(
                (len(matched_skills) / len(jd_skills)) * 100,
                2
            )

        # -----------------------------
        # Final Weighted Score
        # -----------------------------
        final_score = round(
            (0.7 * similarity_percent) + (0.3 * skill_match_percent),
            2
        )

        return {
            "semantic_similarity": similarity_percent,
            "skill_match": skill_match_percent,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "final_score": final_score
        }

    except Exception as e:
        return {"error": str(e)}