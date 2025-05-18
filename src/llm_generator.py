import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()
import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

WEAK_TOPICS = ["force", "motion", "work", "energy", "sound", "pressure", "gravitation"]

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        reader = PdfReader(pdf)
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content
    return text


def get_text_chunks(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    return splitter.split_text(text)


def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = FAISS.from_texts(text_chunks, embedding=embeddings)
    vectorstore.save_local("faiss_index")


def get_conversational_chain():
    prompt_template = """
    You are a helpful tutor for Class IX students. Answer clearly and concisely.
    Use only the information from the context below. If the answer is not found in the context, reply:
    "The answer is not available in the provided context."

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    model = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash-latest",
        temperature=0.4,
        convert_system_message_to_human=True
    )
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain


def match_topic(question):
    for topic in WEAK_TOPICS:
        if topic.lower() in question.lower():
            return topic, True
    return "General", False


def generate_followups(question):
    return [
        f"What is an example related to {question.split()[0].lower()}?",
        f"Why is {question.split()[0].lower()} important?",
        f"Explain {question.split()[0].lower()} in simple words."
    ]


def process_user_query(user_question, profile):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = vector_db.similarity_search(user_question, k=2)

    if not docs:
        return "No relevant information found in the documents.", "", "Unknown", [], False

    context = "\n\n".join([doc.page_content for doc in docs])
    chain = get_conversational_chain()
    output = chain(
        {"input_documents": docs, "question": user_question},
        return_only_outputs=True
    )

    answer = output["output_text"]
    topic, weak_flag = match_topic(user_question)
    followups = generate_followups(user_question)

    return answer, context, topic, followups, weak_flag
