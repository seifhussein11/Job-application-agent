import os
import numpy as np
from sentence_transformers import SentenceTransformer
from agents.state import ApplicationState

MODEL_PATH = "models/scorer_dataset/scorer_checkpoint"



def score_similarity(cv,job_description):
    
    model = SentenceTransformer(MODEL_PATH)
    cv_embedding = model.encode(cv)
    job_description_embedding = model.encode(job_description)
    
    similarity = float(
        np.dot(cv_embedding, job_description_embedding) /
        (np.linalg.norm(cv_embedding) * np.linalg.norm(job_description_embedding))
    )
    
    return round(max(0.0, min(1.0, similarity)), 3)


def run(state : ApplicationState):
    
    print("scoring agent starting")
    
    try:
        
        input_cv = state["input_cv"]
        tailored_cv = state["tailored_cv"]
        job_description = state["job_description"]
        
        print("Scoring original CV")
        
        input_score = score_similarity(input_cv,job_description)
        state["raw_match_score"] = input_score
        
        print(f"Similarity score between original CV and job description: {input_score:.3f}")
        
        
        print("Scoring tailored CV")
        
        tailored_score = score_similarity(tailored_cv,job_description)
        state["tailored_match_score"] = tailored_score
        
        print(f"Similarity score between tailored CV and job description: {tailored_score:.3f}")
        
        improvement = tailored_score - input_score
        
        print(f"Improvement between tailored and original CV: {improvement:+.3f}")
        
        
    except Exception as e:
        print(f"Scoring agent failed: {e}")
        state["error"] = str(e)
        state["status"] = "failed"
        
    return state
        