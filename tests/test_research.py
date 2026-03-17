from agents.orchestrator import run_pipeline

job_description = """

About Sail Reply:
Sail Reply is an AI tech innovation consultancy that delivers experience-led, value-focused solutions for some of the world’s most forward-thinking organisations. Our mission is democratising LLMs to any business process by turning proprietary knowledge into competitive advantage with bespoke LLMs built for Clients domain and deployed at scale. We build bespoke LLM solutions tailored to the client’s business processes, delivering enterprise-grade performance comparable to leading off‑the‑shelf model. Providing a solution designed for high relevance, low latency, and compliance.


Role Overview:
As an AI engineer, you will help deliver experience-led, value-focused solutions for innovative organizations by building bespoke LLMs tailored to client business processes. Your work will focus on turning proprietary knowledge into competitive advantage by deploying custom LLMs at scale, achieving enterprise-grade performance on par with leading off-the-shelf models. These solutions are designed for high relevance, low latency, and strict compliance, ensuring maximum impact for our clients. This role is available for an immediate start.


Responsibilities:
Design, develop, and train large language models and AI systems.
Fine-tune pre-trained LLMs (e.g., GPT, LLaMA, Mistral, Falcon) for specific use cases.
Build and optimize prompting strategies, Retrieval-Augmented Generation (RAG), and agent-based systems.
Prepare, clean, and manage large-scale datasets for model training.
Implement model evaluation, benchmarking, and performance optimization.
Deploy models into production using scalable and secure architectures.
Collaborate with cross-functional teams to translate business needs into AI solutions.
Monitor model performance, manage model drift, iterate improvements, and stay current with the latest research and advancements in AI and LLMs.


About the Candidate:
Bachelor’s or Master’s degree (2:1 or higher) in Computer Science, AI, Machine Learning, or a related field (or equivalent experience) is essential.
Strong experience with Python and ML frameworks such as PyTorch or TensorFlow, and hands-on experience training, fine-tuning, or deploying LLMs.
Solid understanding of NLP, transformers, attention mechanisms, embeddings, and experience with data preprocessing, tokenization, and dataset pipelines.
Familiarity with REST APIs, microservices, model serving, and MLOps tools (e.g., MLflow, Kubeflow, Airflow, Weights & Biases).
Experience with cloud platforms (AWS, GCP, Azure), distributed training, model parallelism, inference optimization, and GPU/TPU infrastructure.
Knowledge of vector databases (e.g., FAISS, Pinecone), security, privacy, and responsible AI practices.
Strong problem-solving, analytical, and communication skills, with a positive, team-oriented attitude and a passion for continuous learning.
Additional advantages include experience with RLHF, open-source contributions, building AI copilots/chatbots, client and stakeholder management, and use of Atlassian tools like Jira and Confluence.
Willingness to travel within the UK and EU for client engagements as required.


Reply is an Equal Opportunities Employer and committed to embracing diversity in the workplace. We provide equal employment opportunities to all employees and applicants for employment and prohibits discrimination and harassment of any type regardless of age, sexual orientation, gender, identity, pregnancy, religion, nationality, ethnic origin, disability, medical history, skin colour, marital status or parental status or any other characteristic protected by the Law. 
 
Reply is committed to making sure that our selection methods are fair to everyone. To help you during the recruitment process, please let us know of any Reasonable Adjustments you may need.

"""

CV = """

Seif Hussein
+44 (0) 7824520763 | arramseif@gmail.com | Cromwell Road, Southampton, SO15 2JF | LinkedIn | GitHub

Profile
Microsoft Certified Azure AI Engineer Associate with an MSc in Artificial Intelligence (Distinction) from the University of Southampton. Specialised in Generative AI, large language models, transformers, and autonomous AI agent systems, with hands-on experience building end-to-end LLM pipelines, multi-stage inference architectures, and agentic workflows. Proficient in prompt engineering, fine-tuning, information extraction, and deploying scalable AI solutions in cloud environments. Proven ability to deliver production-quality AI systems with measurable accuracy outcomes. Seeking a graduate or junior AI Engineer or ML Engineer role.

Education
University of Southampton, Southampton, UK
MSc Artificial Intelligence | Distinction | 2024–2025
Key Modules: Machine Learning Technologies (93%), Foundations of AI (92%), Data Mining (87%), Natural Language Processing (75%), Intelligent Multi-Agents (72%), Computational Finance (71%)
Dissertation: News Classification with Primary Location Extraction using LLMs and Transformers (83%)

University of York, York, UK
BEng Computer Science | First-Class Honours | 2021–2024
Key Modules: Advanced Computer Systems (78%), Machine Learning & Optimisation (79%), Probabilistic & Deep Learning (91%), Search & Representation (83%), Mathematical Foundations of Computer Science (74%), Data Analysis and Management (79%), Networking (84%)
Dissertation: Forecasting Inflation using Deep Learning (80%)

Professional Experience
AI Researcher
Spearfish Security LTD x University of Southampton | Southampton, UK | June 2025 – September 2025
Built an end-to-end autonomous risk analysis system using LLMs and Transformers, automating workflows previously performed manually by security analysts.
Fine-tuned DistilBERT and LLaMA models to classify large-scale news data into 8 predefined risk categories, achieving 85% classification accuracy.
Engineered and benchmarked prompt orchestration strategies including few-shot, chain-of-thought, CRP, and structured prompts to optimise LLM classification and location extraction across pipeline stages.
Developed an LLM-based pipeline to extract fine-granular geographic locations from unstructured text, achieving 97% accuracy at village and town level.
Led model evaluation, error analysis, and iterative optimisation on real-world web-parsed data and communicated findings through technical documentation and presentations.

Cyber Security and Data Leakage Intern
HSBC Bank | Cairo, Egypt | June 2023 – August 2023
Conducted vulnerability assessments and supported improvements to data encryption and data loss prevention systems.
Designed internal cybersecurity training programmes for employees and phishing awareness frameworks for customers.
Researched emerging cyber threats and analysed recent data breach incidents to inform security best practices.

Information Systems Intern
Tayarah Creative Production | Cairo, Egypt | August 2023 – October 2023
Maintained and optimised company databases using MongoDB and SQL.
Wrote and optimised SQL queries to support business reporting and data integrity.
Troubleshot database and system issues in a production environment.

Selected Projects
Inflation Forecasting UK & USA
PyTorch | LSTM | Time Series
Designed and trained a multi-layer LSTM deep learning model for macroeconomic time series forecasting, achieving a 17% reduction in RMSE compared with a baseline ARIMA model. Engineered features from official UK and US economic datasets.

Multi-Agent Maritime Auction System
Python | Autonomous Agents | Game Theory
Designed a competitive multi-agent system where autonomous agents apply game-theoretic bidding strategies to win maritime trade auctions. Implemented agent communication protocols and reward-based decision logic.

Early Alzheimer’s Diagnosis Models
Scikit-learn | PyTorch | Medical ML
Developed and compared multiple supervised models including SVM, Random Forest, and MLP on clinical datasets. Applied feature engineering and SHAP interpretability to identify predictive biomarkers.

Large-Scale Document Clustering
NLP | K-Means | TF-IDF
Built a clustering pipeline over 50,000+ documents using TF-IDF and PCA dimensionality reduction to enable unsupervised topic discovery and document organisation.

Flower Species Classification CNN
PyTorch | CNN | Computer Vision
Built a multi-class CNN classifier using transfer learning with VGG and ResNet backbones, applying augmentation and hyperparameter tuning to improve accuracy.

Certificates
Microsoft Certified Azure AI Engineer Associate | February 2026
Building with the Claude API | March 2026
Microsoft Skills Build NLP Solution with Azure AI Language | February 2026

Technical Skills
Programming: Python, Java, C++, R, SQL
AI and Machine Learning: LLMs, Transformers, Neural Networks, Traditional ML, AI Agents, MCP, NLP, Computer Vision, Information Extraction, Fine-tuning Techniques including LoRA and QLoRA, RAG, Prompt Engineering including Few-shot and Chain-of-Thought, Multi-stage Inference Pipelines, Model Evaluation and Benchmarking, AI Workflows
Frameworks and Tools: PyTorch, TensorFlow, Azure, LangGraph, LangChain, OpenAI API, Claude API, Claude Code, OpenClaw, Git, Hugging Face, Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn

Languages
English: Fluent
Arabic: Native


"""

result = run_pipeline(job_description= job_description, raw_cv= CV)


print("\n" + "="*60)
print("RESEARCH SUMMARY")
print("="*60)
print(f"Company:     {result['company_name']}")
print(f"Role:        {result['job_title']}")
print(f"Tech stack:  {result['tech_stack']}")
print(f"Priorities:  {result['role_priorities']}")

print("\n" + "="*60)
print("TAILORED CV")
print("="*60)
print(result['tailored_cv'])

print("\n" + "="*60)
print("COVER LETTER")
print("="*60)
print(result['cover_letter'])

print("\n" + "="*60)
print("MATCH SCORES")
print("="*60)
print(f"Raw CV score:     {result['raw_match_score']:.3f}")
print(f"Tailored score:   {result['tailored_match_score']:.3f}")
improvement = result['tailored_match_score'] - result['raw_match_score']
print(f"Improvement:      {improvement:+.3f}")

print(result.keys())
print("\n" + "="*60)
print("JUDGE EVALUATION")
print("="*60)
print(f"Judge score:    {result['judge_score']}")
print(f"Approved:       {result['approved']}")
print(f"Revisions:      {result['revision_count']}")
print(f"Feedback:       {result['judge_feedback']}")
print(f"Final status:   {result['status']}")