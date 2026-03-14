import os
from dotenv import load_dotenv
from anthropic import Anthropic
from agents.state import ApplicationState
from tools.web_search import search_multiple
import json

load_dotenv()

client = Anthropic()
used_model = "claude-sonnet-4-5"

def extract_metadata(state: ApplicationState):
    
    response = client.messages.create(
        model= used_model,
        max_tokens= 256,
        messages = [
            {"role" : "user", 
             "content" : f"""
             Extract the company name and the job title from this job description.
             Respond only with a json object like:
             {{"company_name": "...", "job_title": "..."}}
             
             <job_description>
             {state['job_description']}
             </job_description>
             """},
            {"role":"assistant", "content": "```json"}
        ],
        stop_sequences=["```"]
    )
    
    return json.loads(response.content[0].text.strip())


def run_research_searches(company_name, job_title):
    
    queries = [
        f"{company_name} company overview mission",
        f"{company_name} culture work environment",
        f"{company_name} tech stack technologies used",
        f"{company_name} recent news 2025-2026",
        f"{company_name} {job_title} responsibilities requirements",
    ]
    
    search_results = search_multiple(queries)
    
    results = {
        "raw_company_overview": search_results[queries[0]],
        "raw_company_culture": search_results[queries[1]],
        "raw_tech_stack": search_results[queries[2]],
        "raw_recent_news": search_results[queries[3]],
        "raw_role_priorities": search_results[queries[0]],
    }
    

def construct_results(company_name, job_title, raw_results, job_description):
    
    prompt = f"""
    
    You are a career research analyst. You have gathered raw web search results about {company_name} and the role of {job_title}.
    
    Construct the information below into clean, concise summaries for each section.
    Each section should be 3-5 sentences. Be specific — avoid generic filler.
    
    <job_description>
    {job_description}
    </job_description>
    
    <raw_research>
    
        <company_overview>
        {raw_results["raw_company_overview"]}
        </company_overview>
        
        <company_culture>
        {raw_results["raw_company_culture"]}
        </company_culture>
        
        <technical_stack>
        {raw_results["raw_tech_stack"]}
        </technical_stack>
        
        <recent_news>
        {raw_results["raw_recent_news"]}
        </recent_news>
        
        <role_priorities>
        {raw_results["raw_role_priorities"]}
        </role_priorities>
        
    </raw_research>
    
    Respond with ONLY a JSON object with these exact keys:
    {{
    "company_overview": "...",
    "company_culture": "...",
    "tech_stack": "...",
    "recent_news": "...",
    "role_priorities": "..."
    }}
    """
    
    
    response = client.messages.create(
        model = used_model,
        max_tokens= 2048,
        messages = [
            {"role": "user", 
             "content": prompt},
            {"role": "assistant",
             "content": "```json"}
        ],
        stop_sequences=["```"]
    )
    
    return json.loads(response.content[0].text.strip())


def run(state: ApplicationState):
    
    print("research agent starting\n")
    
    try:
        
        print("extracting the company name and title\n")
        
        metadata = extract_metadata(state)
        
        state["company_name"] = metadata["company_name"]
        state["job_title"] = metadata["job_title"]
        
        print(f"Found the Company name: {state['company_name']} and the Job title : {state['job_title']}\n")
        
        print("starting the web search\n")
        
        search_results = run_research_searches(state["company_name"], state["job_title"])
        
        print("Constructing the search results\n")
        
        constructed_search_results = construct_results(state["company_name"], state["job_title"], search_results, state["job_description"])
        
        state["company_overview"] = constructed_search_results["company_overview"]
        state["company_culture"] = constructed_search_results["company_culture"]
        state["tech_stack"] = constructed_search_results["tech_stack"]
        state["recent_news"] = constructed_search_results["recent_news"]
        state["role_priorities"] = constructed_search_results["role_priorities"]
        
        print("research agent completed")
        
    except Exception as e:
        print(f"Research agent failed: {e}")
        state["error"] = str(e)
        state["status"] = "failed"
        
    return state
        
        
    
    
    