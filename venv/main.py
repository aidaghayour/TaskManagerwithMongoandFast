# Import the FastAPI class from the fastapi module

from fastapi import FastAPI, HTTPException
from typing import List
from models import Task
from db import create_task, get_task, get_tasks, update_task,delete_task, TaskInDB  # Import the CRUD functions


# Create an instance of the FastAPI class
app = FastAPI()

# Define a route for the root URL ("/") using the GET method
# Root endpoint to check if the API is running
@app.get("/")
def read_root():
    return {"message": "Welcome to the Task Manager API"}

# Create a new task
@app.post("/tasks/", response_model=TaskInDB)
def create_new_task(task: Task):
    task_id = create_task(task)  # Call create_task to insert the task into the database
    created_task = get_task(task_id)  # Retrieve the created task by its ID
    if created_task:
        return created_task
    raise HTTPException(status_code=404, detail="Task not created")


# Get a single task by ID
@app.get("/tasks/{task_id}", response_model=TaskInDB)
def read_task(task_id: str):
    task = get_task(task_id)  # Retrieve the task by its ID
    if task:
        return task
    raise HTTPException(status_code=404, detail="Task not found")

# Get all tasks
@app.get("/tasks/", response_model=List[TaskInDB])
def read_tasks():
    return get_tasks()  # Retrieve all tasks


# Update a task by ID
@app.put("/tasks/{task_id}", response_model=TaskInDB)
def update_existing_task(task_id: str, task: Task):
    task_in_db = TaskInDB(**task.model_dump(), _id=task_id)
    if not update_task(task_id, task_in_db):
        raise HTTPException(status_code=404, detail="Task not found")
    updated_task = get_task(task_id)
    if updated_task:
        return updated_task
    raise HTTPException(status_code=404, detail="Task not found after update")

# Delete a task by ID
@app.delete("/tasks/{task_id}", response_model=TaskInDB)
def delete_task_endpoint(task_id: str):
    task = get_task(task_id)  # Retrieve the task by its ID
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    delete_task(task_id)  # Delete the task
    return task  # Return the deleted task