import streamlit as st
import tempfile
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from agents.orchestrator import run_pipeline
from tools.cv_parser import parse_CV
from tools.tracker import init_db, save_application

init_db()
st.title("Run Agent")
st.markdown("Upload your CV and paste the job description to generate a tailored application.")

col1, col2 = st.columns(2)

with col1:
    uploaded_cv = st.file_uploader(
        "Upload your CV",
        type=["pdf", "docx"],
        help="Upload a PDF or Word document"
    )
    
    
with col2:
    job_description = st.text_area(
        "Paste the job description",
        height=300,
        placeholder="Paste the full job description here..."
    )
    
if st.button("Generate Application", type="primary", use_container_width=True):
    
    if not uploaded_cv:
        st.error("Please upload your CV.")
    elif not job_description.strip():
        st.error("Please paste a job description.")
    else:
        
        suffix = ".pdf" if uploaded_cv.name.endswith(".pdf") else ".docx"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_cv.read())
            tmp_path = tmp.name
            
        try:
            
            with st.spinner("Parsing CV..."):
                cv_text = parse_CV(tmp_path)
                st.write(f"**Parsed CV length:** {len(cv_text)} words")
                st.write(cv_text[:300])

            
            status_box = st.empty()

            with st.spinner("Running pipeline..."):
                status_box.info("🔍 Research agent running...")
                result = run_pipeline(
                    job_description=job_description,
                    raw_cv=cv_text
                )

            os.unlink(tmp_path)  
            
            if result["status"] == "failed":
                st.error(f"Pipeline failed: {result.get('error')}")
                
            else:
                
                save_application(result)

                st.success("✅ Application generated successfully!")

                st.subheader("Match Scores")
                col1, col2, col3 = st.columns(3)
                col1.metric("Original CV", f"{result['raw_match_score']:.2f}")
                col2.metric(
                    "Tailored CV",
                    f"{result['tailored_match_score']:.2f}",
                    delta=f"+{result['tailored_match_score'] - result['raw_match_score']:.2f}"
                )
                col3.metric("Judge Score", f"{result['judge_score']:.2f}")
                
                st.subheader("Judge feedback on tailored CV and cover letter")

                st.info(f"**Feedback:** {result['judge_feedback']}")
                
                with st.expander("Tailored CV"):
                    st.text(result["tailored_cv"])

                with st.expander("Cover Letter"):
                    st.text(result["cover_letter"])
                    
        except Exception as e:
            st.error(f"Something went wrong: {e}")
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
                
                