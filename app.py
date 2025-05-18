import streamlit as st
from PyPDF2 import PdfReader
from src.llm_generator import process_user_query, get_vector_store, get_text_chunks, get_pdf_text
from src.logger import log_interaction
import os
import tempfile

st.set_page_config(page_title="Class IX Chatbot", layout="wide")
st.title("📘 Chat with NCERT PDFs (Class IX) using Gemini")

# Sidebar for PDF upload and profile selection
with st.sidebar:
    st.header("🔧 Setup")
    user_name = st.text_input("Enter your name", value="Student")
    profile = st.selectbox("Select your profile", ["Class IX - Weak in Physics", "Class IX - Strong in Physics"])

    pdf_docs = st.file_uploader("Upload your NCERT Science PDFs", accept_multiple_files=True)
    if st.button("Submit & Process PDFs"):
        if not pdf_docs:
            st.warning("Please upload at least one PDF.")
        else:
            with st.spinner("Processing PDFs..."):
                try:
                    raw_text = get_pdf_text(pdf_docs)
                    text_chunks = get_text_chunks(raw_text)
                    get_vector_store(text_chunks)
                    st.success("PDFs processed and indexed successfully.")
                except Exception as e:
                    st.error(f"Failed to process PDFs: {str(e)}")

# Main query area
st.divider()
user_question = st.text_input("Ask a question from the PDFs")

if user_question:
    try:
        response, context, topic, follow_ups, weak_topic_flag = process_user_query(user_question, profile)
        
        st.subheader("📢 Answer")
        st.write(response)

        if follow_ups:
            st.markdown("**💡 You can also ask:**")
            for q in follow_ups:
                st.markdown(f"- {q}")

        if context:
            st.markdown("---")
            st.markdown("**📚 Source Context:**")
            st.markdown(f"<div style='font-size: small; color: gray'>{context}</div>", unsafe_allow_html=True)

        # Log interaction
        log_interaction(user_name, topic, weak_topic_flag)

    except Exception as e:
        st.error(f"❌ Error while answering your question: {str(e)}")
