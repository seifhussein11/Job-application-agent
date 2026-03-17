import os
from dotenv import load_dotenv
from anthropic import Anthropic
from agents.state import ApplicationState
import json

load_dotenv()

client = Anthropic()
used_model = "claude-sonnet-4-5"


def judge_agent_feedback(state: ApplicationState):
    
    if state["revision_count"] == 0:
        return ""
    
    feedback = f"""
    This is revision {state['revision_count']}. The previous version was rejected.
    Judge feedback: {state['judge_feedback']}
    Judge score : {state['judge_score']}
    Address this feedback specifically in your rewrite.
    """
    
    return feedback


def tailor_cv(state: ApplicationState):
    feedback = judge_agent_feedback(state)
    
    prompt = f"""
    
    You are an expert CV tailoring assistant. Your job is to rewrite a candidate's CV to better match a specific job description, using research about the company and role.
    
    You must:
    
    - Rewrite bullet points to use language and keywords from the job description
    - Quantify achievements where possible
    - If a profile or a summary section exist, rewrite it by injecting wanted terms from the job description and research
    - Reorder the skills to have the most relevant skills showing first
    - For roles in the experience section, rephrase the responsibilities of every role in a way that matches the job description
    - Keep the CV truthful — only reframe what's already there, never invent experience or education
    - De-emphasise irrelevant content
    - Keep the length of the CV the same, only editing
    
    
    
    Here are two examples of how to rewrite a bullet point:

    EXAMPLE 1:
    Job description keywords: "LLM pipelines, production deployment, scalable inference"
    Original bullet: "Built a text classification system using BERT"
    Rewritten bullet: "Designed and deployed a production-grade LLM inference pipeline using BERT, 
    achieving 85{{%}} classification accuracy at scale"
    
    EXAMPLE 2:
    Job description keywords: "cross-functional collaboration, stakeholder communication"
    Original bullet: "Presented results to the team"
    Rewritten bullet: "Communicated model performance findings and technical trade-offs to 
    cross-functional stakeholders including product and engineering leads"
    
    Now tailor this CV:
    
    <judge_feedback>
    {feedback}
    </judge_feedback>
    
    <job_description>
    {state['job_description']}
    </job_description>

    <research_intelligence>
    
        <company_overview>
        Company overview: {state['company_overview']}
        </company_overview>
        
        <company_culture>
        Company culture: {state['company_culture']}
        </company_culture>
        
        <teck_stack>
        Key tech stack: {state['tech_stack']}
        </teck_stack>
        
        <role_priorities>
        Role priorities: {state['role_priorities']}
        </role_priorities>
        
    </research_intelligence>
    
    
    <original_cv>
    {state['input_cv']}
    </original_cv>
    
    Think step by step:
    1. Identify the top 10 keywords/skills the job description emphasises
    2. Find where in the CV these can be naturally incorporated
    3. Identify which experiences are most relevant to lead with
    4. Plan on how to rephrase the profile/summary section
    5. Plan on how to reorder the skills section
    7. If there is a section for projects, re-order and rewrite the projects to emphasise the keywords and skills identified in job description.
    6. Rewrite the CV with these changes applied
        
    Return ONLY the full rewritten CV text. No commentary, no explanation.
    """
    
    response = client.messages.create(
        model= used_model,
        max_tokens = 2048,
        messages= [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": "Here is the tailored CV:"}
        ]
    )
    
    return response.content[0].text.strip()


def generate_cover_letter(state: ApplicationState):
    feedback = judge_agent_feedback(state)
    
    user_prompt= f"""
    
    You are an expert cover letter writer. Write a compelling, specific cover letter for this candidate applying to this role.
    
    The cover letter must:
    - Be tailored specifically to the job description and company.
    - Open with something specific about the company (use the research intelligence)
    - Connect the candidate's most relevant experience directly to the role priorities
    - Reference the company's tech stack or recent news naturally — not forced
    - Match the company's culture and tone
    - Position the candidate corresponding to the job experience level.
    - Be 3-4 paragraphs, no longer than 350 words
    - Emphasize concrete achievements and specific experiences rather than vague statements
    - Clearly explain why the candidate is interested in this specific company and role
    - Show why the candidate is a strong fit by connecting the experience, skills, education, certificates (Optional) directly to the 
    responsibilities in the job description
    - Sound like a human wrote it — no corporate filler phrases like "I am writing to express 
    my interest" or "I would be a great asset"
    - Write in a natural human tone that feels personal and authentic, avoiding robotic or generic phrasing
    - Do not use cliche or cringey writing
    
    The goal is to produce a compelling cover letter that passes ATS screening and strongly increases the candidate's chances of getting an interview.
    
    <judge_feedback>
    {feedback}
    </judge_feedback>
    
    
    <job_description>
    {state['job_description']}
    </job_description>

    <research_intelligence>
    
        <company_overview>
        Company overview: {state['company_overview']}
        </company_overview>
        
        <company_culture>
        Company culture: {state['company_culture']}
        </company_culture>
        
        <teck_stack>
        Key tech stack: {state['tech_stack']}
        </teck_stack>
        
        <role_priorities>
        Role priorities: {state['role_priorities']}
        </role_priorities>
        
    </research_intelligence>
    
    
    <tailored_cv>
    {state['tailored_cv']}
    </tailored_cv>
    
    
    Write the cover letter now. Return ONLY the cover letter text.
    
    """
    
    
    system_prompt = """
    You are an expert cover letter writer with deep experience in writing successful job applications. 
    Your task is to produce highly tailored, natural sounding cover letters that read as if written by a thoughtful professional.
    
    Follow these rules strictly:
    1. Do not use bold formatting
    2. Do not use the punctuation sign (-)
    3. Structure the letter logically with a strong opening, a focused middle, and a confident closing
    """
    
    response = client.messages.create(
        model = used_model,
        max_tokens= 1000,
        system= system_prompt,
        messages = [
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": "Here is the tailored cover letter:"}
        ]
    )
    
    return response.content[0].text.strip()



def run(state: ApplicationState):
    
    state["tailored_match_score"] = 0.0
    state["judge_score"] = 0.0
    state["approved"] = False
    
    print("tailoring agent started\n")
    
    try:
        
        print("rewriting CV\n")
        state["tailored_cv"] = tailor_cv(state)
        print(f"  → CV tailored ({len(state['tailored_cv'].split())} words)\n")
        
        print("generating cover letter")
        state["cover_letter"] = generate_cover_letter(state)
        print(f"  → Cover letter generated ({len(state['cover_letter'].split())} words)\n")
        
        print("tailoring agent generated")
        
    except Exception as e:
        print(f"Tailoring agent failed {e}")
        state["error"] = str(e)
        state["status"] = "failed"
        
    return state


    