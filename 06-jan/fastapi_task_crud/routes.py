from fastapi import APIRouter, HTTPException
from database import task_collection
from models import Task, UpdateTask
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.get("/")
def root():
    return {"message": "FastAPI is running"}

@router.post("/tasks")
def create_task(task: Task):
    task_data = task.dict()
    task_data["created_at"] = datetime.utcnow()

    result = task_collection.insert_one(task_data)
    return {"id": str(result.inserted_id)}


@router.get("/tasks")
def get_tasks():
    tasks = []
    for task in task_collection.find():
        task["_id"] = str(task["_id"])
        tasks.append(task)
    return tasks


@router.get("/tasks/{task_id}")
def get_task(task_id: str):
    task = task_collection.find_one({"_id": ObjectId(task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task["_id"] = str(task["_id"])
    return task


@router.put("/tasks/{task_id}")
def update_task(task_id: str, task: UpdateTask):
    update_data = {k: v for k, v in task.dict().items() if v is not None}

    if not update_data:
        raise HTTPException(status_code=400, detail="No data provided to update")

    updated = task_collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": update_data}
    )

    if updated.matched_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task updated successfully"}


@router.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    deleted = task_collection.delete_one({"_id": ObjectId(task_id)})

    if deleted.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task deleted successfully"}

@router.get("/tasks/search/")
def search_tasks(completed: bool):
    tasks = []
    for task in task_collection.find({"completed": completed}):
        task["_id"] = str(task["_id"])
        tasks.append(task)
    return tasks