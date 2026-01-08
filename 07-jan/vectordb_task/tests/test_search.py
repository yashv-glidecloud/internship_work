from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_search_returns_multiple_results():
    response = client.get("/vectors/search", params={"query": "Eshan"})
    assert response.status_code == 200

    data = response.json()

    assert "results" in data
    assert isinstance(data["results"], dict)

    results_block = data["results"]
    assert "results" in results_block
    assert isinstance(results_block["results"], list)

    assert results_block["matches_found"] >= 1

    for item in results_block["results"]:
        assert "Eshan" in item["document"]
        assert "distance" in item