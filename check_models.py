import google.generativeai as genai

# ✅ Use your actual Gemini API key
genai.configure(api_key="AIzaSyC353dO9XWDu170gKNfPcotVk9PCPRN6Kg")

# ✅ List models that support generateContent
models = genai.list_models()

for model in models:
    if "generateContent" in model.supported_generation_methods:
        print(f"✅ {model.name} — supports: {model.supported_generation_methods}")
