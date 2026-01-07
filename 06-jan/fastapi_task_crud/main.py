from fastapi import FastAPI
from routes import router

app = FastAPI(title="Task Management API")

@app.get("/")
def root():
    return {"message": "FastAPI Task CRUD API is running"}

app.include_router(router)