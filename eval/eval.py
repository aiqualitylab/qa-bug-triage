import os
import json
import sys
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rag import search_bugs, init_store
from openai import OpenAI

DATASET = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eval_dataset.json")
RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.json")

def get_answer(query, contexts,api_key):
    client = OpenAI(api_key=api_key)    
    context= "\n".join(contexts)
    response = client.chat.completions.create(
            model="gpt-4o",
            tokens=500,
            messages=[{
                    "role": "user",
                    "content": f"Query: {query}\n\nContext:\n{context}\n\nAnswer in 2 sentences:"
                    }]
    )
    return response.choices[0].message.content.strip()

run_eval(api_key):

dataset = json.load(open(DATASET))

print (f"Loaded {len(dataset)} queries from dataset")

init_store()

samples = []

for item in dataset:
    query = item["query"]
    search = search_bugs(query, top_k=5)
    contexts = [f"{b['title']}: {b['description']}" for b in bugs]
    answer = get_answer(query, contexts, api_key)
    samples.append({
        "user_input": query,
        "response": answer,
        "reference": item["reference_answer"],
        "retrieved_contexts": contexts
    })

    print(f" query: {query[:50]}")
    print(f" answer: {answer[:80]}\n")

