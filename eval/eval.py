
import os
import json
import sys
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag import search_bugs, init_store
from openai import OpenAI
from ragas import evaluate, EvaluationDataset, SingleTurnSample
from ragas.metrics import Faithfulness, AnswerRelevancy, ContextPrecision
from ragas.llms import LlamaIndexLLMWrapper
from llama_index.llms.openai import OpenAI as LlamaOpenAI

DATASET = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eval_dataset.json")
RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.json")


def get_answer(query, contexts, api_key):
    client  = OpenAI(api_key=api_key)
    context = "\n".join(contexts)
    resp    = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=150,
        messages=[{
            "role": "user",
            "content": f"Query: {query}\n\nContext:\n{context}\n\nAnswer in 2 sentences:"
        }]
    )
    return resp.choices[0].message.content.strip()


def build_sample(item, api_key):
    query    = item["query"]
    bugs     = search_bugs(query, top_k=5)
    contexts = [f"{b['title']}: {b['description']}" for b in bugs]
    answer   = get_answer(query, contexts, api_key)
    print(f"query : {query}")
    print(f"answer: {answer}\n")
    return SingleTurnSample(
        user_input=query,
        response=answer,
        retrieved_contexts=contexts,
        reference=item["reference_answer"]
    )


def run_eval(api_key):
    dataset = json.load(open(DATASET))
    print(f"Loaded {len(dataset)} queries\n")

    init_store()

    llm           = LlamaOpenAI(model="gpt-4o", api_key=api_key)
    evaluator_llm = LlamaIndexLLMWrapper(llm)

    samples = [build_sample(item, api_key) for item in dataset]

    results = evaluate(
        EvaluationDataset(samples=samples),
        metrics=[
            Faithfulness(llm=evaluator_llm),
            AnswerRelevancy(llm=evaluator_llm),
            ContextPrecision(llm=evaluator_llm),
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
        "faithfulness":      round(float(df["faithfulness"].mean()), 3),
        "answer_relevancy":  round(float(df["answer_relevancy"].mean()), 3),
        "context_precision": round(float(df["context_precision"].mean()), 3),
    }, open(RESULTS, "w"), indent=2)

    print("Saved to eval/results.json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-key", required=True)
    args = parser.parse_args()
    run_eval(args.api_key)