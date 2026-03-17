import streamlit as st
import pandas as pd
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from tools.tracker import get_all_applications, init_db

init_db()

st.title("Application Tracker")

applications = get_all_applications()

if not applications:
    st.info("No applications yet. Run the generation agent to get started.")
    
else:
    
    total = len(applications)
    avg_improvement = sum(
        a["tailored_score"] - a["raw_score"]
        for a in applications
    ) / total
    
    col1, col2 = st.columns(2)
    col1.metric("Total Applications", total)
    col2.metric("Avg Score Improvement", f"+{avg_improvement:.2f}")
    
    st.subheader("All Applications")
    df = pd.DataFrame(applications)
    df = df[[
        "created_at", "company_name", "job_title",
        "raw_score", "tailored_score"
    ]]
    df.columns = [
        "Date", "Company", "Role",
        "Raw Score", "Tailored Score"
    ]
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.subheader("View Application")
    selected_idx = st.selectbox(
        "Select an application",
        options=range(len(applications)),
        format_func=lambda i: f"{applications[i]['company_name']} — {applications[i]['job_title']} ({applications[i]['created_at'][:10]})"
    )

    selected = applications[selected_idx]

    col1, col2 = st.columns(2)
    with col1:
        with st.expander("Tailored CV"):
            st.text(selected["tailored_cv"])
    with col2:
        with st.expander("Cover Letter"):
            st.text(selected["cover_letter"])

    st.info(f"**Judge feedback:** {selected['judge_feedback']}")