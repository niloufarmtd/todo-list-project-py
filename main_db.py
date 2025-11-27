from app.db.session import SessionLocal
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.services.project_service import ProjectService
from app.services.task_service import TaskService

def main():
    db = SessionLocal()
    try:
        project_repo = ProjectRepository(db)
        task_repo = TaskRepository(db)
        project_service = ProjectService(project_repo)
        task_service = TaskService(task_repo)
        
        print("Database version is running!")
        
    finally:
        db.close()

if __name__ == "__main__":
    main()