# QA Bug Triage Pipeline

> A modern RAG workflow for turning messy app reviews into structured, searchable QA bug intelligence.

[Hugging Face Space](https://huggingface.co/spaces/aiqualitylab/qa-bug-triage) · [GitHub Repository](https://github.com/aiqualitylab/qa-bug-triage)

## Overview

Teams often receive product feedback as noisy, repetitive, and unstructured review text. This project converts those reviews into structured bug reports with an LLM, stores them in a local vector database, and makes them easy to search and summarize.

The result is a lightweight bug triage assistant built with Python, Gradio, OpenAI, ChromaDB, and RAG evaluation tooling.

## What It Does

| Capability | Description |
| --- | --- |
| Review collection | Fetches real Google Play reviews |
| Query routing | Classifies incoming text before triage |
| Structured triage | Generates JSON bug reports with consistent fields |
| Hybrid retrieval | Combines semantic retrieval with BM25 keyword matching |
| AI summaries | Produces concise summaries for triage and search results |
| Store reset | Clears persisted bugs directly from the UI |

## Live Demo

- Hugging Face Space: https://huggingface.co/spaces/aiqualitylab/qa-bug-triage
- GitHub Repo: https://github.com/aiqualitylab/qa-bug-triage

## Why This Project

Instead of manually scanning reviews, QA engineers can:

1. collect feedback from a live source,
2. turn it into structured bug records,
3. search recurring issues faster,
4. summarize findings for triage and reporting.

## Core Features

1. Collect real Google Play reviews.
2. Route each review as bug report, feature request, or general complaint.
3. Triage bug reports into structured JSON.
4. Store bug data in ChromaDB.
5. Search with hybrid retrieval using semantic search plus BM25.
6. Generate short AI summaries for triage and search results.
7. Clear stored bugs from the UI.

## Tech Stack

- Python
- Gradio
- OpenAI GPT-4o
- ChromaDB
- rank-bm25
- RAGAS

## API Keys

Required:

1. OpenAI API key

Notes:

1. The app uses BYOK in the UI.
2. The key input is masked.
3. Do not commit API keys into the repository.

## Quick Start

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

## How To Use

1. Open the local Gradio URL after starting the app.
2. Paste your OpenAI API key into the masked BYOK field.
3. Use `Collect` to fetch and triage live reviews.
4. Use `Triage` to analyze one custom review.
5. Use `Search` to retrieve similar bugs.
6. Use `Clear bugs` to reset the store.

## Project Structure

```text
app.py                  # Gradio app and interaction flows
collect.py              # Google Play review collection
triage.py               # Routing and structured triage logic
rag.py                  # Chroma storage and hybrid retrieval
eval/eval.py            # RAG evaluation script
eval/eval_dataset.json  # Evaluation dataset
eval/results.json       # Latest saved evaluation metrics
```

## Evaluation

Included assets:

1. Evaluation script in `eval/eval.py`
2. Evaluation dataset in `eval/eval_dataset.json`
3. Saved metrics in `eval/results.json`

Run evaluation:

```powershell
python eval\eval.py --api-key YOUR_OPENAI_API_KEY
```

Latest results:

| Metric | Score |
| --- | ---: |
| Faithfulness | 0.243 |
| Answer Relevancy | 0.724 |
| Context Precision | 0.050 |

## Cost Estimate

Target: under $0.50 for a short demo session.

Typical low-cost session:

1. One collect run with 5 reviews
2. One manual triage
3. Two search summaries

Expected usage:

1. Around 8k to 20k tokens depending on review length
2. Typically under $0.50 for a short test session

Tips to keep cost low:

1. Keep max reviews between 5 and 10
2. Avoid repeated large collect runs
3. Use short test inputs for validation

## Functionalities Implemented

### Requirements Covered

1. RAG project written in Python
2. Uses at least one LLM
3. Public repository with collection and curation scripts
4. README with project explanation and setup
5. BYOK input in the UI
6. Cost estimate included
7. API key requirements listed
8. More than 5 optional techniques covered

### Techniques Implemented

1. Streaming responses in the UI
2. Dynamic few-shot prompting using similar bugs
3. Evaluation code and dataset included
4. Domain-specific app for QA bug triage
5. Structured JSON data curation for RAG
6. Hybrid retrieval with semantic search and BM25
7. Query routing in the active app flow

## Data Sources

1. Google Play Store reviews via `google-play-scraper`
2. User-entered custom review text in the app