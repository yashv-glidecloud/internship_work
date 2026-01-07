import chromadb
import ollama
import uuid
from data import DOCUMENTS

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="documents")


def embed_text(text: str):
    response = ollama.embeddings(
        model="nomic-embed-text",
        prompt=text
    )
    return response["embedding"]


def initialize_embeddings():
    if collection.count() > 0:
        return

    for doc in DOCUMENTS:
        collection.add(
            ids=[str(uuid.uuid4())],
            documents=[doc],
            embeddings=[embed_text(doc)]
        )


def search_documents(query: str):
    query_embedding = embed_text(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=1
    )

    return results["documents"][0][0]


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