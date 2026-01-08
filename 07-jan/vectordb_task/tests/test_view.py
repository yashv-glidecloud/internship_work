from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_view_vectors():
    response = client.get("/vectors/view")
    assert response.status_code == 200

    data = response.json()
    assert "total_documents" in data
    assert data["total_documents"] > 0
    assert isinstance(data["total_documents"], int)