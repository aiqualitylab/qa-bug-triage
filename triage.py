import json
import uuid
from openai import OpenAI

# ── system prompt ─────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a bug triage assistant who reads customer reviews and extracts structured bug reports.

Your output must always be valid with these exact fields:

{
"title": "A concise title summarizing the bug",
"severity": "One of 'critical', 'major', 'minor', or 'trivial'",
"component": "The app component affected by the bug (e.g., 'login', 'payment', 'UI')",
"platform": "The platform where the bug occurs (e.g., 'Android', 'iOS')",
"frequency_estimate": "An estimate of how often the bug occurs (e.g., 'always', 'often', 'sometimes', 'rarely')",
"symptom": "A detailed description of the symptoms experienced by users",
"user_impact": "A description of how the bug impacts users (e.g., 'prevents login', 'causes crashes', 'leads to data loss')",
"recommendation_label": "A recommended action for the development team (e.g., 'investigate immediately', 'schedule for next release', 'monitor user feedback')",
}

severity guide:
- critical: The bug causes complete failure of a core feature, data loss, or security vulnerabilities. It severely impacts user experience and requires immediate attention.
- high: The bug significantly impairs functionality or causes frequent crashes, but does not result in complete failure. It should be addressed as soon as possible.
- medium: The bug causes noticeable issues or inconveniences but has workarounds available. It should be fixed in a timely manner.
- low: The bug has minimal impact on functionality or user experience, such as minor UI glitches or typos. It can be scheduled for future releases.

Rules:
- Return only the JSON object with the specified fields. Do not include any explanations, apologies, or additional text.
- If review is vague, make your best guess from context.
- Never leave a field empty — use Unknown or Other as fallback."""


# ── function 1: route_review ──────────────────────────────────────────────────

def route_review(review_text: str, api_key: str) -> dict:
    """
    Classifies a raw review into one of three categories BEFORE triaging.
    This is called query routing — optional feature #10.

    Why do this first?
        Not every review is a bug report.
        Some are feature requests, some are vague complaints.
        Routing helps us decide how to handle each one differently.

    Parameters:
        review_text : the raw review string from Google Play
        api_key     : OpenAI API key passed in from the UI — never hardcoded

    Returns:
        {"route": "bug_report", "confidence": 0.97}
        {"route": "feature_request", "confidence": 0.85}
        {"route": "general_complaint", "confidence": 0.91}
    """
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=50,
        messages=[
                    {
                        "role": "user",
                        "content": f"""Classify this review into exactly one category:
                                - bug_report        : describes a crash, freeze, error, or malfunction
                                - feature_request   : asks for something new or improved
                                - general_complaint : vague dissatisfaction, no specific technical issue

                        Reply with JSON only, no explanation:
                        {{"route": "...", "confidence": 0.0}}

                        Review: {review_text}"""
                    }
                ]
            )
    
    raw = response.choices[0].message.content.strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        print(f"Failed to parse routing response: {raw}")
        return {"route": "bug_report", "confidence": 0.8}
