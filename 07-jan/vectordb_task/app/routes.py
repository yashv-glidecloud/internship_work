from fastapi import APIRouter, Query
from app.chroma import search_documents, view_collection

router = APIRouter(prefix="/vectors", tags=["Vectors"])


@router.get("/search")
def search(
    query: str = Query(...)
):
    return {
        "query": query,
        "results": search_documents(query)
    }


@router.get("/view")
def view():
    return view_collection()