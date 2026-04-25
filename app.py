import os
import json
import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI
from collect import fetch_reviews
from triage import triage_review
from rag import init_store, add_bug, search_bugs

load_dotenv()

init_store()

def collect_and_triage(review, api_key):
   similar = search_bugs(review["text"], top_k=2)
   structured = triage_review(review["text"], api_key, similar_bugs=similar)
   add_bug(structured)
   return structured.get("title", "")

def handle_collect(app_name, max_reviews, api_key_input):
    api_key = (api_key_input or "").strip() or os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        yield "OPENAI_API_KEY missing. Add it to .env or enter it in the optional field."
        return

    yield f"Fetching reviews for {app_name}..."
    reviews = fetch_reviews(app_name, max_reviews=int(max_reviews))
    yield f"Got {len(reviews)} reviews. Triaging..."
    titles  = [collect_and_triage(r, api_key) for r in reviews]
    output  = "\n".join([f"{i+1}. {t}" for i, t in enumerate(titles)])
    yield f"Done — {len(reviews)} bugs saved.\n\n{output}"

def build_triage_output(review_text,api_key):
    similar = search_bugs(review_text, top_k=2)
    structured = triage_review(review_text, api_key, similar_bugs=similar)
    add_bug(structured)

    output  = f"Severity: {structured.get('severity','')} | Component: {structured.get('component','')}\n\n"
    output += f"Bug report:\n```json\n{json.dumps(structured, indent=2)}\n```\n\n"
    output += "Similar bugs:\n"
    output += "\n".join([f"- {b.get('title','')} [{b.get('severity','')}]" for b in similar])
    return output, structured

def handle_triage(review_text, api_key_input):
    api_key = (api_key_input or "").strip() or os.getenv("OPENAI_API_KEY", "").strip()
    yield "Triaging review..."
    output, structured = build_triage_output(review_text, api_key)
    yield output

    client = OpenAI(api_key=api_key)
    stream = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=200,
        stream=True,
        messages=[{
            "role": "user",
            "content": f"Write a 3 sentence QA incident summary:\n{json.dumps(structured, indent=2)}"
        }]
    )

    output += "\nAI Summary:\n\n"
    for chunk in stream:
        output += chunk.choices[0].delta.content or ""
        yield output

with gr.Blocks(title="QA Bug Triage") as demo:
    gr.Markdown("# QA Bug Triage Pipeline\nUses OPENAI_API_KEY from .env by default.")

    api_key_box = gr.Textbox(
        label="OpenAI API key (optional override)",
        placeholder="Leave empty to use .env",
        type="password",
        value=""
    )

    with gr.Tabs():

        with gr.TabItem("1. Collect"):
            app_name_box = gr.Textbox(label="App name", value="notion")
            max_box      = gr.Slider(5, 20, value=10, step=5, label="Max reviews")
            collect_btn  = gr.Button("Fetch and triage", variant="primary")
            collect_out  = gr.Markdown()
            collect_btn.click(
                handle_collect,
                [app_name_box, max_box, api_key_box],
                collect_out
            )

        with gr.TabItem("2. Triage"):
            review_box = gr.Textbox(
                label="Paste a review",
                lines=4,
                placeholder="App crashes every time I try to upload a photo..."
            )
            triage_btn = gr.Button("Triage", variant="primary")
            triage_out = gr.Markdown()
            triage_btn.click(
                handle_triage,
                [review_box, api_key_box],
                triage_out
            )

        
if __name__ == "__main__":
    demo.launch()      
    