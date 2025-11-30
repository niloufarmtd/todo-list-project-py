from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
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

@router.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    """
    Get a specific project by ID
    """
    project_repo = ProjectRepository(db)
    project = project_repo.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/projects/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project_data: ProjectUpdate, db: Session = Depends(get_db)):
    """
    Update a project
    """
    project_repo = ProjectRepository(db)
    project = project_repo.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project.name = project_data.name
    project.description = project_data.description
    
    return project_repo.update(project)

@router.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    """
    Delete a project
    """
    project_repo = ProjectRepository(db)
    project = project_repo.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project_repo.delete(project_id)
    return {"message": "Project deleted successfully"}

@router.get("/health")
def health_check():
    return {"status": "healthy", "service": "projects"}


