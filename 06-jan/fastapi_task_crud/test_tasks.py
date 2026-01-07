from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "FastAPI Task CRUD API is running"

def test_create_task():
    response = client.post(
        "/tasks",
        json={
            "title": "Test Task",
            "description": "Testing task creation",
            "completed": False
        }
    )

    assert response.status_code == 200
    assert "id" in response.json()

def test_get_tasks():
    response = client.get("/tasks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_task():
    # Create task first
    create_response = client.post(
        "/tasks",
        json={
            "title": "Update Test",
            "description": "Before update",
            "completed": False
        }
    )

    task_id = create_response.json()["id"]

    # Update task
    update_response = client.put(
        f"/tasks/{task_id}",
        json={"completed": True}
    )

    assert update_response.status_code == 200
    assert update_response.json()["message"] == "Task updated successfully"

def test_delete_task():
    # Create task
    create_response = client.post(
        "/tasks",
        json={
            "title": "Delete Test",
            "description": "To be deleted",
            "completed": False
        }
    )

    task_id = create_response.json()["id"]

    # Delete task
    delete_response = client.delete(f"/tasks/{task_id}")

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Task deleted successfully"