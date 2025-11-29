from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.task_service import TaskService
from app.repositories.task_repository import TaskRepository
from app.exceptions.service_exceptions import TaskNotFoundException

router = APIRouter()

# Get tasks for a specific project
@router.get("/projects/{project_id}/tasks", response_model=List[TaskResponse])
def get_project_tasks(project_id: int, db: Session = Depends(get_db)):
    task_repo = TaskRepository(db)
    return task_repo.get_by_project(project_id)

@router.post("/projects/{project_id}/tasks", response_model=TaskResponse)
def create_task(project_id: int, task_data: TaskCreate, db: Session = Depends(get_db)):
    
    task_repo = TaskRepository(db)
    task_service = TaskService(task_repo)

    task = task_service.create_task(
        title=task_data.title,
        description=task_data.description,
        project_id=project_id,
        deadline=task_data.deadline
    )

# Get specific task
@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task_repo = TaskRepository(db)
    task = task_repo.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
