import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer, InputExample, losses
from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator
from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv

load_dotenv()

DATASET_PATH = "models/scorer_dataset/training_dataset.json"
MODEL_OUTPUT_PATH = "models/scorer_dataset/scorer_checkpoint"
BASE_MODEL = "all-MiniLM-L6-v2"

def load_dataset(path):
    with open(path) as f:
        data = json.load(f)
        
    return data


def prepare_examples(data):
    examples = []
    
    for item in data:
        
        cv = item["cv"].strip()
        job_description = item["job_description"].strip()
        score = float(item["score"])
        
        examples.append(InputExample(texts = [cv, job_description], label = score))
        
    return examples

def train(dataset_path: str = DATASET_PATH, output_path: str = MODEL_OUTPUT_PATH):
    
    data = load_dataset(dataset_path)
    print(f"  → {len(data)} pairs loaded")
    
    examples = prepare_examples(data)
    print("data prepared")
    
    train_examples, test_examples = train_test_split(examples, test_size=0.2, random_state=42)
    
    print("data split")
    
    model = SentenceTransformer(BASE_MODEL)
    print("model loaded")
    
    train_dataloader = DataLoader(train_examples, shuffle= True, batch_size = 16)
    train_loss = losses.CosineSimilarityLoss(model)
    
    test_CV = [t.texts[0] for t in test_examples]
    test_job_description = [t.texts[1] for t in test_examples]
    test_scores = [t.label for t in test_examples]
    
    evaluator = EmbeddingSimilarityEvaluator(sentences1= test_CV, sentences2=  test_job_description,scores=test_scores, name = "cv_jobDes_eval" )
    
    print("Fine-tuning is starting")
    
    model.fit(
        train_objectives=[(train_dataloader,train_loss)],
        evaluator= evaluator,
        epochs= 5,
        evaluation_steps= 50,
        output_path=  output_path,
        show_progress_bar=True
    )
    
    print(f"\n✅ Model saved to {output_path}")
    return model


if __name__ == "__main__":
    train()
    
    