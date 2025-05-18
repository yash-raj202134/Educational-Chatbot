import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
import google.generativeai as genai
from .config import GOOGLE_API_KEY, EMBED_MODEL, LLM_MODEL, INDEX_FOLDER

# Configure Gemini API key
genai.configure(api_key=GOOGLE_API_KEY)

# 🔹 Function to extract text from uploaded PDF documents
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        reader = PdfReader(pdf)
        for page in reader.pages:
            text += page.extract_text()
    return text

# 🔹 Function to split large text into manageable chunks
def get_text_chunks(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    return splitter.split_text(text)

# 🔹 Save the embedded chunks to a local FAISS vector store
def save_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model=EMBED_MODEL)
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local(INDEX_FOLDER)

# 🔹 Load the FAISS vector store from disk
def load_vector_store():
    embeddings = GoogleGenerativeAIEmbeddings(model=EMBED_MODEL)
    return FAISS.load_local(INDEX_FOLDER, embeddings, allow_dangerous_deserialization=True)

# 🔹 Set up Gemini LLM with a custom QA prompt for context-grounded answers
def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context. 
    If the answer is not in the context, say "Answer is not available in the context".
    
    Context:
    {context}
    
    Question:
    {question}
    
    Answer:
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    
    llm = ChatGoogleGenerativeAI(
        model=LLM_MODEL,
        temperature=0.7,
        convert_system_message_to_human=True
    )
    return load_qa_chain(llm, chain_type="stuff", prompt=prompt)

# 🔹 Check if a given question touches on known weak Physics topics
def is_weak_topic(text):
    from .config import WEAK_TOPICS
    return any(topic.lower() in text.lower() for topic in WEAK_TOPICS)

# 🔹 Generate 2–3 follow-up questions based on the last keyword in the user query
def suggest_followups(query):
    topic = query.strip().split()[-1].rstrip("?.,")
    return [
        f"What are the applications of {topic}?",
        f"Can you explain {topic} with an example?",
        f"Why is {topic} important in science?"
    ]
