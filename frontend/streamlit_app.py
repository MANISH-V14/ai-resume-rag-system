import streamlit as st
import requests
import plotly.graph_objects as go

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="AI Resume Screening System",
    layout="wide"
)

# ------------------ CUSTOM STYLING ------------------
st.markdown("""
<style>
.big-font {
    font-size:22px !important;
    font-weight:600;
}
.score-card {
    padding:30px;
    border-radius:20px;
    background: linear-gradient(135deg, #1f77b4, #00c6ff);
    color:white;
    text-align:center;
}
.section-box {
    padding:15px;
    border-radius:12px;
    background-color:#f5f7fa;
}
</style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------
st.title("🧠 AI Resume Screening & RAG Evaluation System")
st.markdown("Semantic + Skill Gap Analysis using Transformer Embeddings")

# ------------------ INPUT SECTION ------------------
col1, col2 = st.columns(2)

with col1:
    resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

with col2:
    job_description = st.text_area(
        "Paste Job Description",
        height=250
    )

# ------------------ ANALYZE BUTTON ------------------
if st.button("🚀 Analyze Resume"):

    if resume_file is None or job_description.strip() == "":
        st.warning("Please upload resume and paste job description.")
    else:
        try:
            with st.spinner("Analyzing resume..."):

                response = requests.post(
                    "http://127.0.0.1:8000/analyze",
                    files={"resume": resume_file},
                    params={"job_description": job_description}
                )

                result = response.json()

            if "error" in result:
                st.error(result["error"])
            else:

                # ------------------ SCORE CARD ------------------
                st.markdown("### 🎯 Overall Candidate Match")

                st.markdown(f"""
                <div class="score-card">
                    <h1>{result['final_score']}%</h1>
                    <p>Final Candidate Match Score</p>
                </div>
                """, unsafe_allow_html=True)

                # ------------------ GAUGE CHART ------------------
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=result["final_score"],
                    title={'text': "Candidate Fit"},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 50], 'color': "#ff4b4b"},
                            {'range': [50, 75], 'color': "#ffa600"},
                            {'range': [75, 100], 'color': "#2ecc71"}
                        ],
                    }
                ))

                st.plotly_chart(fig, use_container_width=True)

                # ------------------ METRICS ------------------
                st.markdown("### 📊 Detailed Breakdown")

                m1, m2 = st.columns(2)

                m1.metric("Semantic Similarity", f"{result['semantic_similarity']}%")
                m2.metric("Skill Match", f"{result['skill_match']}%")

                # ------------------ SKILL SECTIONS ------------------
                st.markdown("### 🛠 Skill Analysis")

                s1, s2 = st.columns(2)

                with s1:
                    st.markdown("#### ✅ Matched Skills")
                    if result.get("matched_skills"):
                        st.success(", ".join(result["matched_skills"]))
                    else:
                        st.write("No strong matches detected.")

                with s2:
                    st.markdown("#### ❌ Missing Skills")
                    if result.get("missing_skills"):
                        st.error(", ".join(result["missing_skills"]))
                    else:
                        st.success("No major skill gaps detected.")

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")