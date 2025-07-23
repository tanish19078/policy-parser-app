import google.generativeai as genai
import os
import json

genai.configure(api_key=os.getenv("GEMINI_API_KEY") or "your-api-key-here")
model = genai.GenerativeModel("gemini-pro")

def make_decision(parsed_query: dict, retrieved_clauses: list) -> dict:
    prompt = f"""
You are a claims approval assistant. Given a structured insurance claim request and relevant clauses, decide:

- Should the procedure be covered? (Yes/No)
- If yes, is any payout mentioned?
- Justify the decision by mapping to exact clause(s) quoted.

Respond in this JSON format:
{{
  "decision": "approved" or "rejected",
  "amount": "optional payout amount",
  "justification": "explanation with clause references"
}}

Structured Query:
{json.dumps(parsed_query, indent=2)}

Relevant Clauses:
{json.dumps(retrieved_clauses, indent=2)}
"""

    response = model.generate_content(prompt)
    try:
        return json.loads(response.text)
    except Exception as e:
        print("❌ Gemini response parse failed:", e)
        print("Raw output:\n", response.text)
        return {
            "decision": "unknown",
            "amount": "N/A",
            "justification": response.text[:1000]  # Show partial fallback
        }
