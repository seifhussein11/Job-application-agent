import stat
from turtle import st
from typing import TypedDict, Optional
from datetime import datetime


class ApplicationState(TypedDict):
    
    job_description : str
    input_cv : str
    job_title : str
    company_name : str
    
    company_overview :str
    company_culture : str
    tech_stack : str
    recent_news : str
    role_priorities : str
    
    tailored_cv : str
    cover_letter : str
    
    raw_match_score : float
    tailored_match_score : float
    
    judge_feedback : str
    judge_score : float
    revision_count : int
    approved : bool
    
    created_at : str
    status : str
    error : Optional[str]
    

def initial_state(job_description : str, input_cv : str):
    
    return ApplicationState(
        job_description= job_description,
        input_cv= input_cv,
        job_title= "",
        company_name= "",
        company_overview= "",
        company_culture= "",
        tech_stack= "",
        recent_news= "",
        role_priorities= "",
        tailored_cv= "",
        cover_letter= "",
        raw_match_score= 0.0,
        tailored_match_score= 0.0,
        judge_feedback= "",
        judge_score = 0.0,
        revision_count= 0,
        approved= False,
        created_at= datetime.now().isoformat,
        status = "running",
        error = None 
    )
    
    