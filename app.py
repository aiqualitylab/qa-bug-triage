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

