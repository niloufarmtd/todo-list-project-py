from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db
from app.schemas.project import ProjectCreate, ProjectResponse
from app.services.project_service import ProjectService
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository

router = APIRouter()

@router.get("/projects", response_model=List[ProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    project_repo = ProjectRepository(db)
    task_repo = TaskRepository(db)
    project_service = ProjectService(project_repo, task_repo)
    
    return project_service.get_all_projects()

@router.post("/projects", response_model=ProjectResponse)
def create_project(project_data: ProjectCreate, db: Session = Depends(get_db)):
    project_repo = ProjectRepository(db)
    task_repo = TaskRepository(db)
    project_service = ProjectService(project_repo, task_repo)
    
    return project_service.create_project(project_data.name, project_data.description)