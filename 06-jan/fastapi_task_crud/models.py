from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Task(BaseModel):
    title: str
    description: str
    completed: bool = False

class UpdateTask(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None