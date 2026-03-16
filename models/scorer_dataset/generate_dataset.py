from calendar import c
import json
import os
import random
import time
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()
used_model = "claude-sonnet-4-5"

ROLE_PAIRS = [

    # ── PERFECT MATCHES (0.92–0.98) ──────────────────────────────
    # Same role, same level — slight wording variation only
    ("Graduate AI Engineer", "Entry-Level AI Engineer", 0.97),
    ("Junior ML Engineer", "Junior Machine Learning Engineer", 0.95),
    ("Graduate Data Scientist", "Entry-Level Data Scientist", 0.96),
    ("Graduate NLP Engineer", "Entry-Level NLP Engineer", 0.95),
    ("Junior AI Researcher", "Graduate AI Research Engineer", 0.93),

    # ── STRONG MATCHES (0.75–0.91) ────────────────────────────────
    # Same domain, one level gap up — candidate is slightly junior for the role
    ("Graduate AI Engineer", "Junior AI Engineer", 0.82),
    ("Junior ML Engineer", "Mid-Level ML Engineer", 0.78),
    ("Graduate Data Scientist", "Junior Data Scientist", 0.85),
    ("Junior NLP Engineer", "Mid-Level NLP Engineer", 0.76),
    ("Graduate Software Engineer", "Junior AI Engineer", 0.75),

    # Same level, closely adjacent roles — high skill overlap
    ("Junior ML Engineer", "Junior AI Engineer", 0.88),
    ("Graduate Data Scientist", "Graduate ML Engineer", 0.84),
    ("Junior NLP Engineer", "Junior LLM Engineer", 0.87),
    ("Junior MLOps Engineer", "Junior ML Engineer", 0.80),
    ("Graduate AI Engineer", "Junior Data Scientist", 0.76),

    # ── MODERATE MATCHES (0.50–0.74) ─────────────────────────────
    # Same domain, two level gap — candidate clearly under-qualified
    ("Graduate AI Engineer", "Mid-Level AI Engineer", 0.60),
    ("Junior ML Engineer", "Senior ML Engineer", 0.52),
    ("Graduate Data Scientist", "Mid-Level Data Scientist", 0.58),
    ("Junior AI Engineer", "Senior NLP Engineer", 0.50),

    # Same level, adjacent but different specialisation
    ("Junior ML Engineer", "Junior Backend Engineer", 0.62),
    ("Graduate Data Scientist", "Graduate Data Analyst", 0.68),
    ("Junior AI Engineer", "Junior DevOps Engineer", 0.55),
    ("Graduate NLP Engineer", "Graduate Computer Vision Engineer", 0.65),
    ("Junior MLOps Engineer", "Junior DevOps Engineer", 0.70),

    # Over-qualified — candidate is senior for a junior role
    ("Senior ML Engineer", "Junior ML Engineer", 0.58),
    ("Mid-Level AI Engineer", "Graduate AI Engineer", 0.62),
    ("Senior Data Scientist", "Junior Data Scientist", 0.55),

    # ── WEAK MATCHES (0.25–0.49) ──────────────────────────────────
    # Same broad tech field, very different specialisation + level gap
    ("Graduate AI Engineer", "Senior Backend Engineer", 0.38),
    ("Junior ML Engineer", "Senior Frontend Engineer", 0.30),
    ("Graduate Data Scientist", "Senior Product Manager", 0.32),
    ("Junior AI Engineer", "Mid-Level QA Engineer", 0.28),
    ("Graduate NLP Engineer", "Senior iOS Engineer", 0.26),

    # Same level, completely different tech specialisation
    ("Junior ML Engineer", "Junior UX Designer", 0.30),
    ("Graduate AI Engineer", "Graduate Cybersecurity Analyst", 0.40),
    ("Junior Data Scientist", "Junior Embedded Systems Engineer", 0.28),

    # ── NO MATCH (0.05–0.24) ──────────────────────────────────────
    # Completely different field regardless of level
    ("Graduate AI Engineer", "Senior Nurse", 0.06),
    ("Junior ML Engineer", "Mid-Level Accountant", 0.08),
    ("Graduate Data Scientist", "Senior Marketing Manager", 0.10),
    ("Junior AI Engineer", "Graduate Civil Engineer", 0.12),
    ("Graduate NLP Engineer", "Senior Chef", 0.05),
]

SCORE_GUIDANCE = {
    "0.92–0.98": "Perfect match. Same role, same level — slight wording variation only.",
    "0.75–0.91" : "Strong match. Either same domain, one level gap up, where candidate is slightly junior for the role, or same level, closely adjacent roles — high skill overlap.",
    "0.50–0.74": "Moderate match. They can be same domain, but two level gap — candidate clearly under-qualified, or same level, adjacent but different specialisation, or over-qualified — candidate is senior for a junior role.",
    "0.25–0.49" : "Weak match. Either same broad tech field, very different specialisation + level gap, or same level, completely different tech specialisation.",
    "0.05–0.24" : "NO MATCH, completely different field regardless of level."
    
}


LEVEL_GUIDANCE = {
    "graduate": {
        "years": "0–1 years (recent graduate)",
        "cv_style": "Lead with education and dissertation. Projects are academic or internship-based. Skills are theoretical with some practical exposure. No leadership experience. Enthusiastic tone.",
        "word_count": "160–200 words",
    },
    "entry-level": {
        "years": "0–1 years",
        "cv_style": "Lead with education and any internships. Mix of academic projects and early professional work. Skills section prominent. No management experience.",
        "word_count": "160–200 words",
    },
    "junior": {
        "years": "1–3 years",
        "cv_style": "Lead with experience. Has shipped real projects in production. Growing technical depth. No team leadership yet. References specific tools and frameworks used professionally.",
        "word_count": "200-240 words",
    },
    "mid-level": {
        "years": "3–6 years",
        "cv_style": "Strong technical ownership. Has led small projects or mentored juniors. Quantified impact (e.g. improved accuracy by X%, reduced latency by Y%). References architectural decisions made.",
        "word_count": "220-260 words",
    },
    "senior": {
        "years": "6+ years",
        "cv_style": "Deep technical expertise and cross-team influence. Has designed systems from scratch. Mentors others. Business impact framing (cost savings, revenue, scale). Selective and concise — only highlights biggest wins.",
        "word_count": "250-300 words",
    },
}


def extract_level(role_title: str) -> str:
    
    role_lower = role_title.lower()
    for level in LEVEL_GUIDANCE:
        if level in role_lower:
            return level
    return "junior" 


def generate_dataset_pair(cv_role, job_descr_role, score):
    
    cv_level = extract_level(cv_role)
    job_level = extract_level(job_descr_role)
    
    cv_guidance = LEVEL_GUIDANCE[cv_level]
    job_guidance = LEVEL_GUIDANCE[job_level]
    
    
    
    
    prompt = f"""
    Generate a realistic CV and job description pair for model training.
    
    
    
    <candidate>
    
        <CV_role>
        {cv_role}
        </CV_role>
        
        <CV_experience>
        {cv_guidance["years"]}
        </CV_experience>
        
        <CV_style>
        {cv_guidance["cv_style"]}
        </CV_style>
        
        <CV_length>
        {cv_guidance["word_count"]}
        </CV_length>
        
    </candidate>
    
    <job_description>
    
        <job_description_role>
        {job_descr_role}
        </job_description_role>
        
        <job_description_level>
        {job_level}
        </job_description_level>
        
        <experience_years_expected>
        {job_guidance["years"]}
        </experience_years_expected>
        
        <job_description_length>
        250 - 300 words
        </job_description_length>
        
    </job_description>   
    
    <score_guidance>
    {SCORE_GUIDANCE}
    </score_guidance>
        
    
    Target Relevance Score : {score} (0.0 = completely irrelevant, 1.0 = perfect match)
    
    Follow these instructions:
    
    -The CV and job description must feel authentic and realistic.
    -The CV language, depth, and framing must clearly reflect a {cv_level} candidate.
    -The job description requirements must clearly reflect expectations for a {job_level} hire.
    -The degree of match between them should feel exactly like: {score}, use the score guidance.
    
    Do NOT mention the score or relevance anywhere in the CV or job description text. 
    
    Respond ONLY with a JSON object:
    {{"cv": "...", "job_description": "...", "score": {score}}}  
    """
    
    response = client.messages.create(
        max_tokens = 1250,
        model = used_model,
        messages = [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": "```json"}
        ],
        stop_sequences=["```"]
        )
    
    text = response.content[0].text.strip()
    return json.loads(text)


def generate_dataset(output_path: str = "models/scorer_dataset/training_dataset.json", no_per_pair : int = 5):
    os.makedirs("models/scorer_dataset", exist_ok=True)
    dataset = []
    
    for cv_role, job_desc_role, base_score in ROLE_PAIRS:
        print(f"Generating pairs: {cv_role} → {job_desc_role} (score ~{base_score})")
        
        for i in range(no_per_pair):
            score = round(min(1.0, max(0.0, base_score + random.uniform(-0.05, 0.05))), 2)
            
            try:
                pair = generate_dataset_pair(cv_role, job_desc_role, score)
                dataset.append(pair)
                print(f"  ✓ Pair {i+1}/{no_per_pair} generated (score: {pair['score']})")
                time.sleep(0.5)  # avoid rate limiting

            except Exception as e:
                print(f"  ✗ Failed to generate pair: {e}")
                continue
            
    with open(output_path, "w") as f:
        json.dump(dataset, f, indent=2)

    print(f"\ Dataset saved: {len(dataset)} pairs → {output_path}")
    return dataset


if __name__ == "__main__":
    generate_dataset(no_per_pair=5)  
            