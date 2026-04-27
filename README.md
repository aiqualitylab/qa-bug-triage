# 🐛 QA Bug Triage Pipeline

> A modern RAG workflow for turning messy app reviews into structured, searchable QA bug intelligence.

[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![OpenAI](https://img.shields.io/badge/GPT--4o-OpenAI-412991?style=flat-square&logo=openai&logoColor=white)](https://openai.com)
[![Gradio](https://img.shields.io/badge/Gradio-UI-orange?style=flat-square&logo=gradio&logoColor=white)](https://gradio.app)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Store-teal?style=flat-square)](https://trychroma.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

**🔗 Links:** [Hugging Face Demo](https://huggingface.co/spaces/aiqualitylab/qa-bug-triage) · [GitHub Repository](https://github.com/aiqualitylab/qa-bug-triage)

---

## 📖 Overview

Teams often receive product feedback as noisy, repetitive, and unstructured review text. This project converts those reviews into structured bug reports with an LLM, stores them in a local vector database, and makes them easy to search and summarize.

The result is a lightweight **bug triage assistant** built with Python, Gradio, OpenAI, ChromaDB, and RAG evaluation tooling.

---

## ✨ What It Does

| Capability | Description |
|---|---|
| 📥 Review collection | Fetches real Google Play reviews |
| 🔀 Query routing | Classifies incoming text before triage |
| 🗂️ Structured triage | Generates JSON bug reports with consistent fields |
| 🔍 Hybrid retrieval | Combines semantic retrieval with BM25 keyword matching |
| 🤖 AI summaries | Produces concise summaries for triage and search results |
| 🗑️ Store reset | Clears persisted bugs directly from the UI |

---

## 🏗️ Architecture

```
Google Play Reviews
        │
        ▼
  ┌─────────────┐
  │ Query Router │  ──→  feature request / general complaint (dropped)
  └─────────────┘
        │ bug report
        ▼
  ┌─────────────┐
  │   Triage    │  ──→  structured JSON bug record
  └─────────────┘
        │
        ▼
  ┌─────────────┐
  │  ChromaDB   │  ──→  vector + BM25 hybrid index
  └─────────────┘
        │
        ▼
  ┌─────────────┐
  │ AI Summary  │  ──→  concise triage output
  └─────────────┘
```

---

## 🚀 Quick Start

```powershell
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Then open the local Gradio URL in your browser.

---

## 🔑 API Keys

This app uses **BYOK (Bring Your Own Key)**:

- Paste your OpenAI API key into the masked field in the UI
- The key input is masked and never committed to the repository

> ⚠️ **Never commit API keys to source control.**

---

## 🖥️ How To Use

1. **Collect** — fetch and triage live Google Play reviews
2. **Triage** — analyze a single custom review
3. **Search** — retrieve similar bugs via hybrid retrieval
4. **Clear bugs** — reset the ChromaDB store

---

## 📁 Project Structure

```
qa-bug-triage/
├── app.py                  # Gradio app and interaction flows
├── collect.py              # Google Play review collection
├── triage.py               # Routing and structured triage logic
├── rag.py                  # Chroma storage and hybrid retrieval
└── eval/
    ├── eval.py             # RAG evaluation script
    ├── eval_dataset.json   # Evaluation dataset
    └── results.json        # Latest saved evaluation metrics
```

---

## 📊 Evaluation

Run the evaluation suite:

```powershell
python eval\eval.py --api-key YOUR_OPENAI_API_KEY
```

**Latest results:**

| Metric | Score | |
|---|---|---|
| Answer Relevancy | `0.724` |
| Faithfulness | `0.243` |
| Context Precision | `0.050` |

---

## 💰 Cost Estimate

**Target:** under `$0.50` for a short demo session.

| Parameter | Value |
|---|---|
| Token range | ~8k – 20k tokens |
| Typical cost | < $0.50 per session |
| Recommended max reviews | 5 – 10 |

**Tips to keep costs low:**
- Keep max reviews between 5 and 10
- Avoid repeated large collect runs
- Use short test inputs for manual triage validation

---

## 🛠️ Tech Stack

| Tool | Role |
|---|---|
| [Python](https://python.org) | Core language |
| [Gradio](https://gradio.app) | Web UI |
| [OpenAI GPT-4o](https://openai.com) | LLM for triage and summaries |
| [ChromaDB](https://trychroma.com) | Vector store |
| [rank-bm25](https://github.com/dorianbrown/rank_bm25) | Keyword retrieval |
| [RAGAS](https://docs.ragas.io) | RAG evaluation framework |
| [google-play-scraper](https://github.com/JoMingyu/google-play-scraper) | Review data source |

---

## ✅ Functionalities Implemented

### Requirements covered

- [x] RAG project written in Python
- [x] Uses at least one LLM
- [x] Public repository with collection and curation scripts
- [x] README with project explanation and setup
- [x] BYOK input in the UI — see [API Keys](#-api-keys)
- [x] Cost estimate included — see [Cost Estimate](#-cost-estimate)
- [x] API key requirements listed — see [API Keys](#-api-keys)
- [x] More than 5 optional techniques covered (7 total — see below)

### Techniques implemented

- [x] Streaming responses in the UI — `app.py`
- [x] Dynamic few-shot prompting using similar bugs — `triage.py`
- [x] Evaluation code and dataset included — `eval/eval.py`, `eval/eval_dataset.json`
- [x] Domain-specific app for QA bug triage — `triage.py`, `app.py`
- [x] Structured JSON data curation for RAG — `triage.py`
- [x] Hybrid retrieval with semantic search and BM25 — `rag.py`
- [x] Query routing in the active app flow — `triage.py`

---

## 📄 License

MIT © [aiqualitylab](https://github.com/aiqualitylab)