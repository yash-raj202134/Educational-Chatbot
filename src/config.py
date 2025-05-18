import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
FAISS_INDEX_PATH = "vector.index"
