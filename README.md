---
title: QA Bug Triage
emoji: 🏆
colorFrom: red
colorTo: yellow
sdk: gradio
sdk_version: "6.12.0"
python_version: "3.10"
app_file: app.py
pinned: false
---    

# QA Bug Triage Pipeline

Simple RAG app for QA teams.

This app collects app-store reviews, converts them into structured bug reports with an LLM, stores them in a vector database, and lets you search and summarize bugs.

## Live Demo

Hugging Face Space (public): 

GitHub Repo: https://github.com/aiqualitylab/qa-bug-triage

## Problem It Solves

Review data is noisy and unstructured. This app helps convert user feedback into searchable bug intelligence.

## Core Features

1. Collect real Google Play reviews.
2. Triage reviews into JSON bug reports.
3. Store bugs in ChromaDB.
4. Search using hybrid retrieval (semantic plus BM25).
5. Generate short AI summaries for triage and search results.
6. Clear all stored bugs from UI.
7. Route review text before triage (bug report vs feature request vs general complaint).

## Tech Stack

1. Python
2. Gradio UI
3. OpenAI GPT-4o
4. ChromaDB
5. rank-bm25
6. RAGAS (evaluation)

## API Keys Required

1. OpenAI API key

Important:
1. Do not commit API keys.
2. This project uses BYOK in UI (user pastes key in app).

## Quick Start

1. Create and activate virtual environment.
2. Install dependencies.
3. Run app.

Windows PowerShell example:

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py

## How To Use

1. Open the local Gradio URL after running app.py.
2. Paste your OpenAI API key in the masked BYOK field.
3. Use tab 1 Collect to fetch and triage reviews.
4. Use tab 2 Triage for one custom review.
5. Use tab 3 Search to retrieve related bugs.
6. Use tab 4 Clear bugs to reset the store.

## Project Structure

1. app.py: Gradio app and workflows.
2. collect.py: Google Play review collection.
3. triage.py: Structured JSON bug extraction.
4. rag.py: Chroma storage and hybrid search.
5. eval/eval.py: RAG evaluation script.
6. eval/eval_dataset.json: Evaluation dataset.

## Evaluation

This project includes:
1. Evaluation script in eval/eval.py
2. Evaluation dataset in eval/eval_dataset.json
3. Metrics: Faithfulness, Answer Relevancy, Context Precision

Run evaluation:

python eval\eval.py --api-key YOUR_OPENAI_API_KEY

Latest results:
 Faithfulness      : 0.243
 Answer Relevancy  : 0.724
 Context Precision : 0.050 

## Cost Estimate (Target: $0.50 or less)

Typical low-cost demo session:
1. 1 collect run with 5 reviews
2. 1 manual triage
3. 2 search summaries

Estimated OpenAI usage:
1. Around 8k to 20k tokens total depending on review length
2. Estimated cost is typically below $0.50 for a short demo session

Tips to keep cost low:
1. Keep max reviews at 5 to 10
2. Avoid repeated large collect runs
3. Use short test inputs for triage/search checks

## Functionalities Implemented

Necessary constraints covered:
1. RAG project written in Python
2. Uses at least one LLM (OpenAI)
3. Public repository with data collection and curation scripts
4. README with project explanation and setup
5. BYOK input in UI (masked OpenAI key field)
6. Cost estimate section under $0.50 target for short demo usage
7. API key requirements listed
8. Optional techniques list included (at least 5)
9. Streaming responses in UI.
10. Dynamic few-shot prompting using similar bugs.
11. Evaluation code and dataset included.
12. Domain-specific app (QA bug triage).
13. Structured JSON data curation for advanced RAG.
14. Hybrid search (semantic plus BM25).
15. Query routing in active app flow (non-bug routes are skipped in storage).

## Data Sources

1. Google Play Store reviews via google-play-scraper.
2. User-entered custom review text in the app.