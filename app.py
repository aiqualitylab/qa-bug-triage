import os
import gradio as gr
from dotenv import load_dotenv
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

def handle_collect(app_name, max_reviews, api_key):
    yield f"Fetching reviews for {app_name}..."
    reviews = fetch_reviews(app_name, max_reviews=int(max_reviews))
    yield f"Got {len(reviews)} reviews. Triaging..."
    titles  = [collect_and_triage(r, api_key) for r in reviews]
    output  = "\n".join([f"{i+1}. {t}" for i, t in enumerate(titles)])
    yield f"Done — {len(reviews)} bugs saved.\n\n{output}"

with gr.Blocks(title="QA Bug Triage") as demo:
    gr.Markdown("# QA Bug Triage Pipeline\nPaste your OpenAI API key to begin.")
    
    default_api_key = os.getenv("OPENAI_API_KEY", "")
    api_key_box = gr.Textbox(
    label="OpenAI API key",
    placeholder="sk-...",
    type="password",
    value=default_api_key
    )

    with gr.Tabs():
        app_name_box = gr.Textbox(label="App name", value="notion")
        max_box      = gr.Slider(5, 50, value=10, step=5, label="Max reviews")
        collect_btn  = gr.Button("Fetch and triage", variant="primary")
        collect_out  = gr.Markdown()
        collect_btn.click(
            handle_collect,
            [app_name_box, max_box, api_key_box],
            collect_out
            )
        
if __name__ == "__main__":
    demo.launch()      
    