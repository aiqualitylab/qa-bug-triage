import json
import gradio as gr
from openai import OpenAI
from collect import fetch_reviews
from triage import route_review, triage_review
from rag import init_store, add_bug, search_bugs, clear_store

init_store()

def collect_and_triage(review, api_key):
    review_text = review["text"]
    route_data = route_review(review_text, api_key)
    route = route_data.get("route", "bug_report")

    if route != "bug_report":
        return None, route

    similar = search_bugs(review_text, top_k=2)
    structured = triage_review(review_text, api_key, similar_bugs=similar)
    add_bug(structured)
    return structured.get("title", ""), route

def handle_collect(app_name, max_reviews, api_key_input):
    api_key = (api_key_input or "").strip()
    if not api_key:
        yield "OpenAI API key is required for BYOK."
        return

    yield f"Fetching reviews for {app_name}..."
    reviews = fetch_reviews(app_name, max_reviews=int(max_reviews))
    yield f"Got {len(reviews)} reviews. Triaging..."

    titles = []
    skipped = {"feature_request": 0, "general_complaint": 0}
    for review in reviews:
        title, route = collect_and_triage(review, api_key)
        if route == "bug_report" and title:
            titles.append(title)
        elif route in skipped:
            skipped[route] += 1

    output = "\n".join([f"{i+1}. {t}" for i, t in enumerate(titles)])
    yield (
        f"Done — {len(titles)} bugs saved. "
        f"Skipped: {skipped['feature_request']} feature request(s), "
        f"{skipped['general_complaint']} general complaint(s).\n\n{output}"
    )

def build_triage_output(review_text,api_key):
    route_data = route_review(review_text, api_key)
    route = route_data.get("route", "bug_report")

    if route != "bug_report":
        confidence = route_data.get("confidence", 0)
        output = (
            f"Route: {route} (confidence: {confidence})\n\n"
            "This input is not a bug report, so it was not added to bug store."
        )
        return output, None

    similar = search_bugs(review_text, top_k=2)
    structured = triage_review(review_text, api_key, similar_bugs=similar)
    add_bug(structured)

    output  = f"Severity: {structured.get('severity','')} | Component: {structured.get('component','')}\n\n"
    output += f"Bug report:\n```json\n{json.dumps(structured, indent=2)}\n```\n\n"
    output += "Similar bugs:\n"
    output += "\n".join([f"- {b.get('title','')} [{b.get('severity','')}]" for b in similar])
    return output, structured

def handle_triage(review_text, api_key_input):
    api_key = (api_key_input or "").strip()
    if not api_key:
        yield "OpenAI API key is required for BYOK."
        return

    yield "Triaging review..."
    output, structured = build_triage_output(review_text, api_key)
    yield output

    if not structured:
        return

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
def build_search_output(results, query):
    output = f"{len(results)} results for: {query}\n\n---\n"
    output += "\n\n---\n".join([
        f"{r.get('title','')}\n"
        f"{r.get('severity','')} | {r.get('component','')} | {r.get('platform','')}\n"
        f"{r.get('description','')}"
        for r in results
    ])
    return output


def get_ai_summary(results, query, api_key):
    client  = OpenAI(api_key=api_key)
    context = "\n".join([
        f"- {r.get('title','')}: {r.get('description','')}"
        for r in results
    ])
    resp = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=150,
        messages=[{
            "role": "user",
            "content": f"Query: {query}\nBugs:\n{context}\nSummarise in 2 sentences:"
        }]
    )
    return resp.choices[0].message.content


def handle_search(query, api_key_input):
    api_key = (api_key_input or "").strip()
    if not api_key:
        return "OpenAI API key is required for BYOK."

    results = search_bugs(query, top_k=5)
    output  = build_search_output(results, query)
    output += f"\n\nAI Summary:\n{get_ai_summary(results, query, api_key)}"
    return output


def handle_clear_bugs():
    removed = clear_store()
    init_store()
    return f"Cleared {removed} bug(s)."

with gr.Blocks(title="QA Bug Triage") as demo:
    gr.Markdown("# QA Bug Triage Pipeline\nBYOK in UI.")

    api_key_box = gr.Textbox(
        label="OpenAI API key (BYOK)",
        placeholder="sk-...",
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

        with gr.TabItem("3. Search"):
            search_box = gr.Textbox(
                label="Search query",
                placeholder="login crash android"
            )
            search_btn = gr.Button("Search", variant="primary")
            search_out = gr.Markdown()
            search_btn.click(
                handle_search,
                [search_box, api_key_box],
                search_out
            )

        with gr.TabItem("4. Clear bugs"):
            clear_btn = gr.Button("Clear stored bugs", variant="stop")
            clear_out = gr.Markdown()
            clear_btn.click(
                handle_clear_bugs,
                outputs=clear_out
            )

        
if __name__ == "__main__":
    demo.launch()      
    