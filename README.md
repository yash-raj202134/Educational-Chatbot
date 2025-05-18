# 📚 Class IX NCERT PDF Chatbot using Gemini API

This project is an interactive chatbot built with **Streamlit**, **LangChain**, and **Google Gemini 1.5 Flash API**. It allows **Class IX students** to upload NCERT science textbooks (PDFs) and ask questions based on their content. The chatbot retrieves relevant context and gives concise, grounded answers with personalized support based on the student's profile (e.g., weak in Physics).

---

## 🚀 Features

- ✅ Upload and process multiple NCERT PDF files
- ✅ Ask questions directly from PDF content
- ✅ Get concise, context-aware answers using Gemini 1.5 Flash
- ✅ See **source context** displayed below each answer
- ✅ Personalized support via **user profile selection** (e.g., weak in Physics)
- ✅ Suggests **follow-up questions** for better learning
- ✅ Logs each interaction with:
  - User name
  - Matched topic
  - Whether a **weak Physics topic** was covered

---

## 🧠 Weak Topics List
Used to personalize feedback and log comprehension challenges:
- `Force`, `Motion`, `Work`, `Energy`, `Sound`, `Pressure`, `Gravitation`

---

## 🗂 Folder Structure
```
project-root/
│
├── app.py # Main Streamlit app
├── .env # API key config
├── requirements.txt # Dependencies
├── logs/
│ └── query_log.csv # Logged queries
├── src/
│ ├── llm_generator.py # LLM logic, embeddings, context retrieval
| └── config.py # Configuration api keys
│ └── logger.py # CSV logging logic
```

## 🔁 Workflow

1. **Upload PDFs**: Users upload NCERT Class IX Science PDFs via the sidebar.
2. **Text Extraction**: Text is extracted from all PDF pages.
3. **Chunking**: Extracted text is split into overlapping chunks for better context retrieval.
4. **Embedding**: Chunks are converted into vector embeddings using `embedding-001` (Google).
5. **Vector Store**: Embeddings are saved in a local FAISS vector database.
6. **User Question**: The user inputs a natural language query.
7. **Context Retrieval**: Top matching chunks are retrieved using similarity search.
8. **LLM Response**: Gemini 1.5 Flash generates a concise, grounded answer.
9. **Personalization**: User profile (e.g., weak in Physics) tailors depth and tone.
10. **Follow-up Suggestions**: 2–3 relevant follow-up questions are generated.
11. **Logging**: The query, matched topic, username, and weak-topic flag are logged.

---

## 🧩 Future Improvements

- Support math questions with LaTeX rendering  
- Enable chatbot memory across multiple turns  
- Visualize PDF topic coverage  
- Admin dashboard for monitoring weak topics  

---

## 🛠️ Built With

- Streamlit  
- LangChain  
- Google Generative AI (Gemini)  
- FAISS  

---

## 🧑‍🏫 Educational Goal

Designed to help Class IX students better understand science topics by enabling conversational learning directly from their textbooks. It aims to reinforce weak areas and encourage curiosity through suggested follow-up questions.
