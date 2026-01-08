import uuid
import chromadb
import ollama
from typing import List
from app.data import DOCUMENTS

CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "documents"
EMBED_MODEL = "mxbai-embed-large"
TOP_K = 5

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)


def embed_text(text: str) -> List[float]:
    response = ollama.embeddings(
        model=EMBED_MODEL,
        prompt=text
    )
    return response["embedding"]


def initialize_embeddings() -> None:
    """
    Idempotent initialization.
    Embeds documents only once.
    """
    if collection.count() > 0:
        return

    ids = [str(uuid.uuid4()) for _ in DOCUMENTS]
    embeddings = [embed_text(doc) for doc in DOCUMENTS]

    collection.add(
        ids=ids,
        documents=DOCUMENTS,
        embeddings=embeddings
    )


def search_documents(query: str, max_results: int = 5, threshold: float = 0.75):
    query_embedding = embed_text(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=max_results,
        include=["documents", "distances"]
    )

    documents = results["documents"][0]
    distances = results["distances"][0]

    filtered_results = []

    for doc, dist in zip(documents, distances):
        if dist <= threshold:
            filtered_results.append({
                "document": doc,
                "distance": dist
            })

    return {
        "query": query,
        "matches_found": len(filtered_results),
        "results": filtered_results
    }


def view_collection():
    data = collection.get(include=["documents", "embeddings"])

    result = []
    for i in range(len(data["ids"])):
        embedding = data["embeddings"][i]

        result.append({
            "id": data["ids"][i],
            "document": data["documents"][i],
            "embedding_length": len(embedding),
            "embedding_preview": [float(x) for x in embedding[:10]]
        })

    return {
        "total_documents": len(result),
        "data": result
    }