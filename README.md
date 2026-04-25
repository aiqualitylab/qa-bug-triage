# QA Bug Triage Pipeline

A RAG-powered app that collects real Google Play reviews, triages them into structured bug reports using GPT-4o, and lets you search them using hybrid semantic and keyword search.

## What it does

1. Fetches real reviews from Google Play Store
2. Triages each review into a structured bug report using GPT-4o
3. Stores bug reports in a local vector database
4. Lets you search bugs using hybrid search (semantic + BM25)