import sys
import os

current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '../../'))
sys.path.insert(0, project_root)

from app.db.session import SessionLocal
from app.repositories.task_repository import TaskRepository

from app.services.task_service import TaskService

def autoclose_overdue_tasks():
    db = SessionLocal()
    try:
        task_repo = TaskRepository(db)
        task_service = TaskService(task_repo)
        
        closed_count = task_service.close_overdue_tasks()
        print(f"Closed {closed_count} overdue tasks")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    autoclose_overdue_tasks()