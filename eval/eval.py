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
