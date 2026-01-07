from fastapi import APIRouter, Query
from chroma import search_documents, view_collection

router = APIRouter(prefix="/vectors", tags=["Vectors"])


@router.get("/search")
def search(query: str = Query(..., example="Who lives in Wagholi?")):
    return {
        "query": query,
        "result": search_documents(query)
    }


@router.get("/view")
def view():
    return view_collection()