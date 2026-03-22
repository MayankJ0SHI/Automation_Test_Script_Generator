from langchain_openai import OpenAIEmbeddings
import hashlib
from dotenv import load_dotenv
from config.settings import settings

load_dotenv()

EMBED_MODEL = settings.EMBED_MODEL
embedding_model = OpenAIEmbeddings(model=EMBED_MODEL)

def get_embedding(text: str) -> list[float]:
    """Generate embedding using LangChain's OpenAIEmbeddings."""
    return embedding_model.embed_query(text)

def hash_text(text: str) -> str:
    """Generate SHA-256 hash of the text (used as unique ID)."""
    return hashlib.sha256(text.encode()).hexdigest()