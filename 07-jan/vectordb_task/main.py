from fastapi import FastAPI
import chromadb
import ollama
from fastapi import UploadFile, File
import uuid

app = FastAPI(title="Vector DB with Chroma + Ollama")

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="documents")

def embed_text(text: str):
    response = ollama.embeddings(
        model="nomic-embed-text",
        prompt=text
    )
    return response["embedding"]

def chunk_text(text: str):
    return [s.strip() for s in text.split(".") if s.strip()]

@app.get("/")
def root():
    return {"message": "Vector DB API is running"}

@app.post("/embed")
def embed_document(text: str):
    chunks = chunk_text(text)

    for i, chunk in enumerate(chunks):
        embedding = embed_text(chunk)
        collection.add(
            ids=[str(uuid.uuid4())],
            embeddings=[embedding],
            documents=[chunk]
        )

    client.persist()

    return {"message": f"{len(chunks)} chunks embedded successfully"}


@app.post("/embed-file")
async def embed_file(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8")

    chunk_size = 500
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    ids = [str(uuid.uuid4()) for _ in chunks]

    embeddings = [
        ollama.embeddings(model="nomic-embed-text", prompt=chunk)["embedding"]
        for chunk in chunks
    ]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids
    )

    client.persist()

    return {"chunks_stored": len(chunks)}


@app.get("/search")
def search_document(query: str):
    query_embedding = embed_text(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=1
    )

    return {
    "query": query,
    "result": results["documents"][0]
}