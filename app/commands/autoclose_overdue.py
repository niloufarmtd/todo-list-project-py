import sys
import os
from datetime import datetime

# Only modify path if not running as module
if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(current_dir, '../../../'))
    if project_root not in sys.path:
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
        
        # Log with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if closed_count > 0:
            print(f"[{timestamp}] ✅ Closed {closed_count} overdue tasks")
        else:
            print(f"[{timestamp}] ℹ️ No overdue tasks found")
        
        return closed_count
        
    except Exception as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] ❌ Error: {e}")
        return 0
    finally:
        db.close()

if __name__ == "__main__":
    autoclose_overdue_tasks()