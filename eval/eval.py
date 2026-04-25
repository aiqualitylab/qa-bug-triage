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

def run_eval(api_key):

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

from ragas import evaluate, EvalutionDataset, SingleTurnSample
from ragas.metrics import Faithfulness, AnswerRelevancy, ContextPrecision
from ragas.llms import LlamaIndexLLMWrapper
from llama_index.llms.openai import OpenAI as LlamaOpenAI

llm = LlamaIndexLLMWrapper(LlamaOpenAI(api_key=api_key, model   ="gpt-4o"))
evaluator_llm = LlamaIndexLLMWrapper(llm)

ragas_samples = [
    SingleTurnSample(
            user_input=s["user_input"],
            response=s["response"],
            retrieved_contexts=s["retrieved_contexts"],
            reference=s["reference"]
    )
    for s in samples
]

results = evaluate(
    EvalutionDataset(samples = ragas_samples),
    metrics = [
        Faithfulness(llm = evaluator_llm),
        AnswerRelevancy(llm = evaluator_llm),
        ContextPrecision(llm = evaluator_llm)
    ]
)

df = results.to_pandas()
print("=" * 40)
print("RAGAS RESULTS")
print("=" * 40)
print(f"Faithfulness      : {df['faithfulness'].mean():.3f}")
print(f"Answer Relevancy  : {df['answer_relevancy'].mean():.3f}")
print(f"Context Precision : {df['context_precision'].mean():.3f}")
print("=" * 40)

json.dump({
        "faithfulness": round(float(df['faithfulness'].mean()), 3),
        "answer_relevancy": round(float(df['answer_relevancy'].mean()), 3),
        "context_precision": round(float(df['context_precision'].mean()), 3),
        }, open(RESULTS, "w"), indent=2)

print (f"Saved results to eval/results.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run RAGAS evaluation on app reviews")
    parser.add_argument("--api_key", required=True)
    args = parser.parse_args()
    run_eval(args.api_key)

