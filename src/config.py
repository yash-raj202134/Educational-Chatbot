import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
EMBED_MODEL = "models/embedding-001"
LLM_MODEL = "gemini-1.5-flash-latest"
INDEX_FOLDER = "faiss_index"
WEAK_TOPICS = [
    "motion", "force", "laws of motion", "gravitation", "work and energy",
    "sound", "floatation", "pressure", "inertia", "acceleration"
]
