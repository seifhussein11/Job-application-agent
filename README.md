AI Job Application Agent

An autonomous multi-agent system that takes a job description and your CV, researches the company, tailors your application, scores the match using a fine-tuned model, and tracks everything in a Streamlit dashboard.

Built with LangGraph, Claude API, and a fine-tuned relevance scoring model.

---

## What It Does

1. **Researches the company** — autonomously gathers information about the employer, role, and culture from the web
2. **Tailors your CV and cover letter** — rewrites bullet points, adjusts keyword density, and restructures content to match the job description
3. **Scores the match** — a fine-tuned DistilBERT model predicts relevance between your CV and the job description (trained on 1000+ CV-JD pairs)
4. **Judges the output** — a judge agent evaluates the tailoring quality and loops back for up to 2 revision cycles if the score is below threshold
5. **Tracks applications** — all runs are logged in a Streamlit dashboard with status, match scores, and output file links

---

##  Architecture

```
User Input (JD + CV)
        │
        ▼
Orchestrator Agent (LangGraph)
        │
   ┌────┼────────────────┐
   ▼    ▼                ▼
Research  Tailoring    Scoring
 Agent     Agent        Agent
   │         │        (fine-tuned)
   └────┬────┘            │
        └────────┬─────────┘
                 ▼
           Judge Agent
           (eval + loop)
                 │
        ┌────────┴──────────┐
        ▼                   ▼
 Tailored Documents   Application Tracker
 (CV + Cover Letter)  (Streamlit Dashboard)
```

---

##  Tech Stack

| Component | Technology |
|---|---|
| Agent orchestration | LangGraph, LangChain |
| LLM backbone | Claude API (claude-sonnet) |
| Relevance scoring | sentence-transformers |
| Web research | Tavily Search API |
| PDF I/O | PyMuPDF, ReportLab |
| UI & tracking | Streamlit, SQLite |
| Model hosting | HuggingFace Hub |

---

##  Project Structure

```
job-application-agent/
├── agents/
│   ├── orchestrator.py       # LangGraph state machine
│   ├── research_agent.py     # Company + role research
│   ├── tailoring_agent.py    # CV + cover letter rewrite
│   ├── scoring_agent.py      # Fine-tuned relevance scoring
│   └── judge_agent.py        # Quality eval + feedback loop
├── models/
│   ├── train_scorer.py       # Fine-tuning script
│   ├── evaluate_scorer.py    # Benchmark evaluation
│   └── scorer_dataset/       # CV-JD relevance pairs
├── tools/
│   ├── web_search.py         # Tavily search wrapper
│   ├── pdf_parser.py         # CV ingestion
│   └── pdf_generator.py      # Output document creation
├── ui/
│   ├── app.py                # Streamlit entry point
│   ├── pages/
│   │   ├── 1_run_agent.py    # Input form + live agent log
│   │   └── 2_tracker.py      # Application tracker dashboard
├── eval/
│   ├── benchmark.py          # End-to-end eval suite
│   └── benchmark_data/       # 30 annotated JD+CV examples
├── tests/
├── requirements.txt
└── README.md
```

---



##  Fine-tuned Scoring Model

The scoring agent uses a Sentence-transformer model fine-tuned on CV–job description pairs labelled with relevance scores (0.0–1.0).






Metrics tracked:
- Scoring model Pearson correlation vs human labels
- Tailoring quality (LLM-as-judge 1–5 scale)
- Keyword coverage improvement (% increase in JD keyword overlap)
- Judge agent loop rate (% of runs requiring revision)

---



**Seif Hussein**  
MSc Artificial Intelligence (Distinction) — University of Southampton  
Microsoft Certified Azure AI Engineer Associate  
[LinkedIn](https://linkedin.com) · [GitHub](https://github.com)
