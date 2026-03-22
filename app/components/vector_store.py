# vector_store.py
import chromadb
from chromadb.config import Settings
from chromadb import PersistentClient
from .embedding import get_embedding, hash_text
from .text_splitter import chunk_code
from config.settings import settings

# -----------------------------------------------------------------------------
# CONFIG ----------------------------------------------------------------------

CHROMA_DIR = settings.CHROMA_PERSIST_DIR  # e.g. "./chroma_data"

# -----------------------------------------------------------------------------
# HELPERS ---------------------------------------------------------------------

def _collection_has_vectors(collection) -> bool:
    """Check if collection already contains any vectors."""
    try:
        return collection.count() > 0
    except Exception:
        return False

def _get_client() -> PersistentClient:
    """Initialize and return a ChromaDB client."""
    return PersistentClient(
        path=CHROMA_DIR,
        settings=Settings(anonymized_telemetry=False)
    )

# -----------------------------------------------------------------------------
# PUBLIC API ------------------------------------------------------------------

def get_or_create_collection(project_name: str):
    """
    Retrieve or create a vector collection for the given project.
    """
    client = _get_client()
    collection_name = project_name.strip().lower().replace(" ", "_")

    existing_collections = [col.name for col in client.list_collections()]
    if collection_name in existing_collections:
        return client.get_collection(name=collection_name)

    print(f"📦 Creating new collection: '{collection_name}'")
    return client.create_collection(name=collection_name)

def embed_and_store(files: list, project_name: str):
    """
    Embed the code chunks and store them in a persistent vector DB collection.

    - Only runs if collection is not already populated.
    - Reuses existing vectors if present.
    """
    client = _get_client()
    collection_name = project_name.strip().lower().replace(" ", "_")

    if collection_name in [col.name for col in client.list_collections()]:
        collection = client.get_collection(name=collection_name)
    else:
        print(f"📦 Creating new collection: '{collection_name}'")
        collection = client.create_collection(name=collection_name)

    if _collection_has_vectors(collection):
        print(f"⚠️  Collection '{collection_name}' already populated — skipping embedding.")
        return collection

    print(f"🧠 Embedding and storing chunks for collection '{collection_name}'...")

    for file in files:
        chunks = chunk_code(file["content"])
        for i, chunk in enumerate(chunks):
            chunk_id = hash_text(f"{file['path']}_{i}")
            try:
                embedding = get_embedding(chunk)
                collection.add(
                    documents=[chunk],
                    embeddings=[embedding],
                    metadatas=[{"path": file["path"], "chunk_id": i}],
                    ids=[chunk_id],
                )
            except chromadb.errors.DuplicateIDError:
                print(f"⏩ Skipping duplicate ID: {chunk_id}")
            except Exception as e:
                print(f"❌ Error embedding chunk {chunk_id}: {e}")

    return collection
