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
    """
    Get all projects
    
    Returns a list of all projects in the system
    Includes task count for each project
    """
    project_repo = ProjectRepository(db)
    task_repo = TaskRepository(db)
    project_service = ProjectService(project_repo, task_repo)
    
    return project_service.get_all_projects()

@router.post("/projects", response_model=ProjectResponse)
def create_project(project_data: ProjectCreate, db: Session = Depends(get_db)):
    """
    Create a new project
    
    - **name**: Project name (max 30 characters)
    - **description**: Project description (max 150 characters)
    
    Returns the created project object
    """
    project_repo = ProjectRepository(db)
    task_repo = TaskRepository(db)
    project_service = ProjectService(project_repo, task_repo)
    
    return project_service.create_project(project_data.name, project_data.description)

@router.get("/health")
def health_check():
    return {"status": "healthy", "service": "projects"}