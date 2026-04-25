import json
import gradio as gr
from openai import OpenAI
from collect import fetch_reviews
from triage import route_review, triage_review
from rag import init_store, add_bug, search_bugs

init_store()

def collect_and_triage(review, api_key):
   similar = search_bugs(review["text"], top_k=2)
   structured = triage_review(review["text"], api_key, similar_bugs=similar)
   add_bug(structured)
   return structured.get("title", "")

def handle_collect(app_name, max_reviews, api_key):
    yield f"Fetching reviews for {app_name}..."
    reviews = fetch_reviews(app_name, max_reviews=int(max_reviews))
    yield f"Got {len(reviews)} reviews. Triaging..."
    titles  = [collect_and_triage(r, api_key) for r in reviews]
    output  = "\n".join([f"{i+1}. {t}" for i, t in enumerate(titles)])
    yield f"Done — {len(reviews)} bugs saved.\n\n{output}"