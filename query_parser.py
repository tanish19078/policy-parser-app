import google.generativeai as genai
import os

# Load Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY") or "your-api-key-here")

model = genai.GenerativeModel("gemini-pro")

def parse_user_query(query: str) -> dict:
    prompt = f"""
    Parse the following insurance claim query and extract:
    - Age
    - Gender
    - Procedure
    - Location
    - Policy duration in months

    Output JSON with keys: age, gender, procedure, location, policy_duration_months

    Query: "{query}"
    """

    response = model.generate_content(prompt)
    try:
        # Extract JSON from Gemini's response
        import json
        parsed = json.loads(response.text)
        return parsed
    except Exception as e:
        print("❌ Failed to parse Gemini response:", e)
        print("Raw response:\n", response.text)
        return {}
