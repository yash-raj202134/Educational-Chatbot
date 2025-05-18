import streamlit as st
from src.llm_generator import (
    get_pdf_text, get_text_chunks, save_vector_store, load_vector_store,
    get_conversational_chain, is_weak_topic, suggest_followups
)
from src.logger import log_query
import os

# Set Streamlit page configuration
st.set_page_config("NCERT Class IX Science Chatbot")
st.title("📚 Chat with Class 9 Science PDFs")

def main():
    # Initialize vector store flag based on existing FAISS index
    if "db_ready" not in st.session_state:
        st.session_state.db_ready = os.path.exists("faiss_index/index.faiss")
    
    # Sidebar: user info and upload controls
    st.sidebar.title("📂 Upload PDFs or Rebuild Index")
    user_name = st.sidebar.text_input("👤 Enter your name", value="Class IX Student")
    profile = st.sidebar.radio("Your Physics Level", ["Weak", "Strong"], index=0)

    # Upload PDFs
    uploaded_pdfs = st.sidebar.file_uploader("Upload PDF(s)", accept_multiple_files=True)

    # Button to rebuild FAISS index from uploaded PDFs
    if st.sidebar.button("Rebuild Index"):
        if uploaded_pdfs:
            with st.spinner("Processing PDFs..."):
                # Extract text → chunk → vector store → save
                raw_text = get_pdf_text(uploaded_pdfs)
                chunks = get_text_chunks(raw_text)
                save_vector_store(chunks)
                st.session_state.db_ready = True
                st.success("Index Rebuilt!")
        else:
            st.warning("Please upload PDFs first.")

    st.divider()

    # Main input box for questions
    question = st.text_input("🔎 Ask a question from your PDFs")

    # Only run if PDFs are indexed and question is provided
    if question and st.session_state.db_ready:
        with st.spinner("Generating answer..."):
            # Load FAISS vector store and search for relevant chunks
            db = load_vector_store()
            docs = db.similarity_search(question)

            # Run LLM chain on retrieved docs + question
            chain = get_conversational_chain()
            response = chain({"input_documents": docs, "question": question}, return_only_outputs=True)

            answer = response["output_text"]

            # Display answer
            st.markdown(f"### ✅ Answer:\n{answer}")
            st.markdown("---")

            # Generate and display follow-up questions
            followups = suggest_followups(question)
            if followups:
                st.markdown("#### 💡 Follow-up Questions")
                for q in followups:
                    st.markdown(f"- {q}")

            st.markdown("---")

            # Display source context (PDF content chunks)
            st.markdown("#### 📄 Source Context (from PDF)")
            for doc in docs:
                st.markdown(f"<small>{doc.page_content}</small>", unsafe_allow_html=True)

            # Log the query: user, matched topic, and weak-topic flag
            log_query(
                user_name=user_name,
                question=question,
                matched_topic=question,
                is_weak=is_weak_topic(question)
            )

    elif question and not st.session_state.db_ready:
        st.error("Please upload and process your PDFs first.")

# Entry point
if __name__ == "__main__":
    main()
