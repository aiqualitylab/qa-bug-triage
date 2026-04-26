# QA Bug Triage Pipeline

Simple RAG app for QA teams.

This app collects app-store reviews, converts them into structured bug reports with an LLM, stores them in a vector database, and lets you search and summarize bugs.

## Live Demo

Hugging Face Space (public): 

GitHub Repo: 

## Problem It Solves

Review data is noisy and unstructured. This app helps convert user feedback into searchable bug intelligence.

## Core Features

1. Collect real Google Play reviews.
2. Triage reviews into JSON bug reports.
3. Store bugs in ChromaDB.
4. Search using hybrid retrieval (semantic plus BM25).
5. Generate short AI summaries for triage and search results.
6. Clear all stored bugs from UI.

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

## Optional Functionalities Implemented

1. Streaming responses in UI.
2. Dynamic few-shot prompting using similar bugs.
3. Evaluation code and dataset included.
4. Domain-specific app (QA bug triage).
5. Structured JSON data curation for advanced RAG.
6. Hybrid search (semantic plus BM25).
7. Query routing helper available in code.

## Data Sources

1. Google Play Store reviews via google-play-scraper.
2. User-entered custom review text in the app.