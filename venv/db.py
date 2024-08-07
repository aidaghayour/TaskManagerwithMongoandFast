from pymongo import MongoClient
from pymongo.collection import Collection
from pydantic import BaseModel
from typing import List, Optional
from models import Task

MONGO_URI = "mongodb://localhost:27017"
DATABASE_NAME = "taskmanager"
COLLECTION_NAME = "tasks"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# This model mirrors the Pydantic Task model but is used for interacting with MongoDB.
class TaskInDB(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    _id: Optional[str] = None  # MongoDB document ID


def create_task(task: Task):
    task_in_db = TaskInDB(**task.model_dump()) #**task.model_dump(): Unpacks the dictionary into keyword arguments for the TaskInDB constructor
    result = collection.insert_one(task_in_db.model_dump())
    return str(result.inserted_id)

def get_task(task_id: str) -> Optional[TaskInDB]:
    task = collection.find_one({"_id": task_id})
    if task:
        return TaskInDB(**task)  # Convert MongoDB document to TaskInDB model
    return None

def get_tasks() -> List[TaskInDB]:
    tasks = list(collection.find())
    return [TaskInDB(**task) for task in tasks]  # Convert each document to TaskInDB model

def update_task(task_id: str, task: TaskInDB) -> bool:
    result = collection.update_one({"_id": task_id}, {"$set": task.model_dump()})
    return result.modified_count > 0

def delete_task(task_id: str) -> bool:
    result = collection.delete_one({"_id": task_id})
    return result.deleted_count > 0
