# from fastapi import FastAPI, UploadFile, File
# import chromadb
# import ollama
# import uuid

# app = FastAPI(title="Vector DB with Chroma + Ollama")

# # -------------------- Chroma Setup --------------------
# client = chromadb.PersistentClient(path="./chroma_db")
# collection = client.get_or_create_collection(name="documents")

# # -------------------- Helpers --------------------
# def embed_text(text: str):
#     response = ollama.embeddings(
#         model="nomic-embed-text",
#         prompt=text
#     )
#     return response["embedding"]

# def chunk_text(text: str):
#     return [s.strip() for s in text.split(".") if s.strip()]

# # -------------------- Routes --------------------
# @app.get("/")
# def root():
#     return {"message": "Vector DB API is running"}

# # -------------------- Embed Text --------------------
# @app.post("/embed")
# def embed_document(text: str):
#     chunks = chunk_text(text)

#     for chunk in chunks:
#         collection.add(
#             ids=[str(uuid.uuid4())],
#             documents=[chunk],
#             embeddings=[embed_text(chunk)]
#         )

#     return {"chunks_embedded": len(chunks)}

# # -------------------- Embed File --------------------
# @app.post("/embed-file")
# async def embed_file(file: UploadFile = File(...)):
#     content = await file.read()
#     text = content.decode("utf-8")

#     chunk_size = 500
#     chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

#     ids = [str(uuid.uuid4()) for _ in chunks]
#     embeddings = [embed_text(chunk) for chunk in chunks]

#     collection.add(
#         ids=ids,
#         documents=chunks,
#         embeddings=embeddings
#     )

#     return {"chunks_stored": len(chunks)}

# # -------------------- Search --------------------
# @app.get("/search")
# def search_document(query: str):
#     query_embedding = embed_text(query)

#     results = collection.query(
#         query_embeddings=[query_embedding],
#         n_results=1
#     )

#     return {
#         "query": query,
#         "result": results["documents"][0][0] if results["documents"] else None
#     }

# # -------------------- VIEW / CHROMADB VIEWER --------------------
# @app.get("/view")
# def view_database():
#     data = collection.get(include=["documents", "embeddings"])

#     result = []

#     for i in range(len(data["ids"])):
#         embedding = data["embeddings"][i]

#         result.append({
#             "id": data["ids"][i],
#             "document": data["documents"][i],
#             "embedding_length": len(embedding),
#             "embedding_preview": [float(x) for x in embedding[:10]]
#         })

#     return {
#         "total_documents": len(result),
#         "data": result
#     }

from fastapi import FastAPI
from routes import router
from chroma import initialize_embeddings

app = FastAPI(title="Vector Embedding Demo")

app.include_router(router)


@app.on_event("startup")
def startup_event():
    initialize_embeddings()


@app.get("/")
def root():
    return {"message": "Vector DB API is running"}
