import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF
from fpdf import FPDF
import io

# ========================
# CONFIG
# ========================
genai.configure(api_key="your_real_api_key_here")  # Replace with your actual API key
model = genai.GenerativeModel(model_name="models/gemini-2.5-flash")


# ========================
# HELPERS
# ========================

def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()


def save_chat_to_pdf(chat_history):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for i, chat in enumerate(chat_history):
        pdf.multi_cell(0, 10, f"Q{i+1}: {chat['question']}")
        pdf.multi_cell(0, 10, f"A{i+1}: {chat['answer']}")
        pdf.ln(5)

    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer


# ========================
# SESSION STATE INIT
# ========================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "combined_text" not in st.session_state:
    st.session_state.combined_text = ""

# ========================
# UI
# ========================
st.set_page_config(page_title="Policy Q&A", page_icon="📄")
st.title("📄 Multi-PDF Insurance Assistant (Gemini 2.5 Flash)")

uploaded_files = st.file_uploader("📤 Upload one or more insurance policy PDFs", type="pdf", accept_multiple_files=True)

# ========================
# TEXT EXTRACTION
# ========================
if uploaded_files:
    combined_text = ""
    for uploaded_file in uploaded_files:
        with st.spinner(f"🔍 Extracting: {uploaded_file.name}"):
            combined_text += extract_text_from_pdf(uploaded_file) + "\n\n"
    st.session_state.combined_text = combined_text[:30000]  # Keep first 30k chars to stay safe with Gemini

if st.session_state.combined_text:
    user_input = st.chat_input("💬 Ask a question about the policies")

    if user_input:
        with st.spinner("🤔 Gemini is thinking..."):
            prompt = f"""
You are an insurance policy assistant. Based on the following document(s), answer the question clearly and concisely:

Q: {user_input}

Document content:
{st.session_state.combined_text}
"""
            response = model.generate_content(prompt)
            answer = response.text

            st.session_state.chat_history.append({
                "question": user_input,
                "answer": answer
            })

    # ========================
    # SHOW CHAT HISTORY
    # ========================
    if st.session_state.chat_history:
        st.divider()
        st.markdown("### 💬 Chat History")
        for i, chat in enumerate(st.session_state.chat_history):
            with st.chat_message("user"):
                st.markdown(f"**Q{i+1}:** {chat['question']}")
            with st.chat_message("assistant"):
                st.markdown(f"**A{i+1}:** {chat['answer']}")

        # Option to download as PDF
        with st.expander("⬇️ Export Chat as PDF"):
            pdf_data = save_chat_to_pdf(st.session_state.chat_history)
            st.download_button("Download Chat", pdf_data, file_name="chat_history.pdf", mime="application/pdf")

else:
    st.info("Upload at least one PDF to begin.")
