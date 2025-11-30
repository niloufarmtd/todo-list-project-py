from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.task_service import TaskService
from app.repositories.task_repository import TaskRepository
from app.models.task import Task

router = APIRouter()

@router.get("/projects/{project_id}/tasks", response_model=List[TaskResponse])
def get_project_tasks(project_id: int, db: Session = Depends(get_db)):
    """
    Get all tasks for a specific project
    
    - **project_id**: ID of the project
    
    Returns list of tasks belonging to the project
    """
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

    return task

@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task_repo = TaskRepository(db)
    task = task_repo.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db)):
    task_repo = TaskRepository(db)
    task = task_repo.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
   
    task.title = task_data.title
    task.description = task_data.description
    task.deadline = task_data.deadline
    if task_data.status:
        task.status = task_data.status
    
    return task_repo.update(task)

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task_repo = TaskRepository(db)
    task = task_repo.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_repo.delete(task_id)
    return {"message": "Task deleted successfully"}

@router.patch("/tasks/{task_id}/status")
def update_task_status(task_id: int, status: str, db: Session = Depends(get_db)):
    task_repo = TaskRepository(db)
    task_service = TaskService(task_repo)
    
    task = task_service.change_task_status(task_id, status)
    return task

@router.post("/tasks/autoclose-overdue")
def autoclose_overdue_tasks(db: Session = Depends(get_db)):
    task_repo = TaskRepository(db)
    task_service = TaskService(task_repo)
    
    closed_count = task_service.close_overdue_tasks()
    return {"message": f"Closed {closed_count} overdue tasks"}
