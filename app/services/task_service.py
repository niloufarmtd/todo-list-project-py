from datetime import datetime
from app.exceptions.service_exceptions import (
    TaskNotFoundException, 
    InvalidTaskStatusException,
    PastDeadlineException
)

class TaskService:
    def __init__(self, task_repository):
        self.task_repo = task_repository
    
    def close_overdue_tasks(self):
        overdue_tasks = self.task_repo.get_overdue_tasks()
        closed_count = 0
        
        for task in overdue_tasks:
            task.status = "done"
            task.closed_at = datetime.now()
            self.task_repo.update(task)
            closed_count += 1
        
        return closed_count
    
    def change_task_status(self, task_id: int, new_status: str):
        valid_statuses = ["todo", "doing", "done"]
        if new_status not in valid_statuses:
            raise InvalidTaskStatusException(new_status)
        
        task = self.task_repo.get_by_id(task_id)
        if not task:
            raise TaskNotFoundException(task_id)
        
        task.status = new_status
        if new_status == "done":
            task.closed_at = datetime.now()
        
        return self.task_repo.update(task)
    
    def validate_deadline(self, deadline_str: str):
        if deadline_str:
            try:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
                if deadline < datetime.now():
                    raise PastDeadlineException()
                return deadline
            except ValueError:
                raise ValueError("❌ Invalid date format! Please use YYYY-MM-DD")
        return None
    
    def delete_task(self, task_id: int):
        task = self.task_repo.get_by_id(task_id)
        if not task:
            raise TaskNotFoundException(task_id)
        
        return self.task_repo.delete(task_id)