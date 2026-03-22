import tiktoken
from config.settings import settings

CHUNK_SIZE = settings.CHUNK_SIZE
CHUNK_OVERLAP = settings.CHUNK_OVERLAP
EMBED_MODEL = settings.EMBED_MODEL

tokenizer = tiktoken.encoding_for_model(EMBED_MODEL)

def chunk_code(content):
    tokens = tokenizer.encode(content)
    chunks = []
    for i in range(0, len(tokens), CHUNK_SIZE - CHUNK_OVERLAP):
        chunk_tokens = tokens[i:i + CHUNK_SIZE]
        chunk = tokenizer.decode(chunk_tokens)
        chunks.append(chunk)
    return chunks
