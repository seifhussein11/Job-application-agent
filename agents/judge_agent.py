import os
from dotenv import load_dotenv
from anthropic import Anthropic
from agents.state import ApplicationState
import json

load_dotenv()

client = Anthropic()
used_model = "claude-sonnet-4-5"
APPROVAL_THRESHOLD = 0.70
MAX_REVISIONS = 2

def evaluate_output(state: ApplicationState):
    
    
    prompt= f"""
    
    You are a professional senior recruiter evaluating a tailored job application.
    Score the quality of this tailored CV and cover letter on a scale of 0.0 to 1.0.
    
    Evaluate each criterion carefully, then give an overall weighted score.

    --- CRITERION 1: CV Quality (25%) ---
    - Are bullet points rewritten using specific language and keywords from the JD?
    - Is the most relevant experience positioned first?
    - Are achievements quantified where possible?
    - Does the skills section reflect the JD's required tech stack?
    Score this 0.0–1.0.

    --- CRITERION 2: Truthfulness & Integrity (20%) ---
    - Does the CV only reframe existing experience — never invent skills or roles?
    - Are claimed technologies ones the candidate demonstrably used in their experience and projects?
    - Does the cover letter make claims consistent with what the CV shows?
    - Flag any statements that appear exaggerated or fabricated.
    Score this 0.0–1.0. A score below 0.5 here should block approval regardless of other scores.

    --- CRITERION 3: Cover Letter Personalisation (20%) ---
    - Does the opening reference something specific about the company (not generic praise)?
    - Does it mention the company's product, mission, recent news, or tech stack naturally?
    - Does it avoid generic filler phrases like "I am writing to express my interest"?
    - Does it show the genuine interest of the candidate in the role and company?
    Score this 0.0–1.0.

    --- CRITERION 4: Candidate-Role Fit Narrative (20%) ---
    - Does the cover letter connect the candidate's specific experience to the role priorities?
    - Does it tell a coherent story of why THIS candidate suits THIS role?
    - Is there a clear thread from the candidate's background to the company's needs?
    Score this 0.0–1.0.

    --- CRITERION 5: Coherence & Professionalism (15%) ---
    - Does the CV read naturally — not keyword-stuffed or robotic?
    - Does the cover letter flow well across paragraphs?
    - Is the tone appropriate for the company culture?
    Score this 0.0–1.0.

    
    --- Inputs ---
    --- INPUTS ---

    <job_description>
    {state['job_description']}
    </job_description>

    <role_priorities>
    {state['role_priorities']}
    </role_priorities>

    <company_culture>
    {state['company_culture']}
    </company_culture>

    <tailored_cv>
    {state['tailored_cv']}
    </tailored_cv>

    <cover_letter>
    {state['cover_letter']}
    </cover_letter>
    
    --- SCORING ---
    Current numeric match score: {state['tailored_match_score']}
    Revision number: {state['revision_count']}

    Think through each criterion step by step.
    Compute the overall score as:
    (cv_quality * 0.25) + (truthfulness * 0.20) + (personalisation * 0.20) + (fit_narrative * 0.20) + (coherence * 0.15)

    Set approved=true only if:
    - Overall score >= 0.75, AND
    - Truthfulness score >= 0.50, AND
    - Numeric match score >= 0.60

    Respond ONLY with a JSON object:
    {{
    "score": 0.0,
    "feedback": "...",
    "approved": false
    }}

    The feedback field should be 4-5 sentences of specific, actionable critique that the tailoring agent can act on in a revision.
    """
    
    response = client.messages.create(
        model = used_model,
        max_tokens = 1024,
        messages = [
            {"role": "user", "content": prompt},
            {"role": "assistant","content":"```json"}
        ],
        stop_sequences=["```"])
    
    return json.loads(response.content[0].text.strip())


def run(state: ApplicationState):
    
    print("judge agent starting")
    
    try:
        
        result = evaluate_output(state)
        
        state["judge_feedback"] = result["feedback"]
        state["judge_score"] = result["score"]
        
        print(f"  → Judge score: {result['score']:.2f}")
        print(f"  → Feedback: {result['feedback'][:100]}...")
        
        if state["revision_count"] >= MAX_REVISIONS:
            print(f"  → Max revisions reached — force approving")
            state["approved"] = True
        else:
            state["approved"] = result["approved"]

        if state["approved"]:
            print("Judge approved the output.")
            state["status"] = "approved"
        else:
            print("Judge requesting revision...")
            state["revision_count"] += 1
    
    
    except Exception as e:
        print(f"❌ Judge agent failed: {e}")
        state["error"] = str(e)
        state["status"] = "failed"

    return state
    