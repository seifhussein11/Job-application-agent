import streamlit as st

st.set_page_config(page_title="Job Applications Tool",page_icon="🤖", layout= "wide")

st.title("Job Application Tool")

st.markdown("""
Paste a job description, upload your CV, and let the agent tailor your
application automatically and show if you are a good match.

**Navigate using the sidebar:**
- **Run Agent** — submit a new application
- **Tracker** — view all past applications
""")

