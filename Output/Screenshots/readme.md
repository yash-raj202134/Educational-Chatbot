# 🤖 Class IX Science Educational Chatbot

This chatbot allows Class 9 students to interactively learn Science concepts from NCERT textbooks. It processes uploaded PDFs (like NCERT books), builds a searchable index using embeddings, and provides grounded answers using Google’s Gemini LLM. It also identifies weak topics (like fundamental Physics concepts), offers follow-up questions, and logs all interactions for educational insights.

---

## 🛠️ Tech Stack & Libraries

| Category              | Tools/Libraries Used                                           |
|-----------------------|---------------------------------------------------------------|
| **Frontend/UI**       | [Streamlit](https://streamlit.io)                             |
| **LLM**               | [Google Gemini 1.5 Flash](https://ai.google.dev) via LangChain |
| **Embeddings**        | `GoogleGenerativeAIEmbeddings`                                |
| **Vector Store**      | [FAISS](https://github.com/facebookresearch/faiss)            |
| **PDF Parsing**       | `PyPDF2`                                                       |
| **Text Splitting**    | `langchain.text_splitter.RecursiveCharacterTextSplitter`      |
| **Prompting & QA**    | `langchain.chains.question_answering`                         |
| **Environment Config**| `.env` and `os.environ`                                       |
| **Logging**           | Custom `logger.py` saving to `logs/query_log.csv`             |

---

## 📂 Project Structure

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


---

## 📌 Assumptions Made

- User uploads valid, readable **Class IX NCERT Science PDFs**.
- Weak topic detection is based on **a predefined list** (e.g., laws of motion, energy, etc.).
- FAISS index is **cached** and reused if already present in `faiss_index/`.
- Follow-up questions are generated based on **keyword from user query**, not semantic chaining.
- Google Gemini API key is configured in `.env` file as `GOOGLE_API_KEY`.

---

## 🚀 Improvements Possible

- ✅ Support **LaTeX rendering** for Math answers.
- ✅ Enable **chat memory** across multiple questions.
- ✅ Topic-wise visualization from PDF to ensure coverage.
- ✅ Admin dashboard for **weak topic frequency** and performance tracking.
- ✅ Multi-turn Q&A chaining.
- ✅ Summarization of PDFs into chapter-level notes.

---

## 🧪 Sample Input/Output Logs (from `query_log.csv`)

| user_name       | question                             | matched_topic        | is_weak_topic |
|------------------|---------------------------------------|----------------------|----------------|
| Yash             | What is Newton's third law?          | Newton's third law  | ✅             |
| Class IX Student | Define energy                        | energy               | ✅             |
| Rahul            | How does sound travel in air?        | sound travel         | ❌             |
| Student A        | Explain gravitational force          | gravitational force  | ✅             |
| Ananya           | Describe chemical reactions          | chemical reactions   | ❌             |

---

## 🧑‍🎓 Educational Goal

This chatbot aims to:
- Help Class IX students **understand NCERT Science** through conversational learning.
- Strengthen **weak foundational topics**, especially in Physics.
- Encourage **curiosity** through automatically suggested follow-up questions.
- Offer a **teacher-like assistant** that’s grounded in official curriculum material.

---
