from fastapi import FastAPI
from app.routes import router
from app.chroma import initialize_embeddings

app = FastAPI(title="Vector Embedding API")

app.include_router(router)


@app.on_event("startup")
def startup_event():
    initialize_embeddings()


@app.get("/")
def root():
    return {"message": "Vector DB API is running"}