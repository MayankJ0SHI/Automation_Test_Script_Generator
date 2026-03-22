from .embedding import get_embedding
from .vector_store import get_or_create_collection

def search_code(query: str, project_name: str, top_k: int = 5):
    """
    Perform a semantic search for the given query within the project's collection.
    
    Args:
        query (str): Natural language query or code snippet.
        project_name (str): The name of the project/collection.
        top_k (int): Number of top results to return.

    Returns:
        Tuple[List[str], List[dict]]: Matched code chunks and associated metadata.
    """
    query_embedding = get_embedding(query)
    collection = get_or_create_collection(project_name)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )
    return results["documents"][0], results["metadatas"][0]
