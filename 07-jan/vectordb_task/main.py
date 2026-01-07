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
