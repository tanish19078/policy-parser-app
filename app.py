import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF
import tempfile

# Configure Gemini
genai.configure(api_key="AIzaSyC353dO9XWDu170gKNfPcotVk9PCPRN6Kg")
model = genai.GenerativeModel(model_name="models/gemini-2.5-flash")

# PDF loader
def extract_text(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()

# UI
st.title("📄 Policy Q&A with Gemini 2.5 Flash")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    with st.spinner("Extracting content..."):
        text = extract_text(uploaded_file)

    question = st.text_input("Ask a question about the policy:")
    
    if question:
        with st.spinner("Thinking..."):
            prompt = f"""
            Based on the following insurance policy content, answer:

            Q: {question}

            Content:
            {text[:1000000]}
            """
            response = model.generate_content(prompt)
            st.markdown("### 💬 Answer:")
            st.write(response.text)
