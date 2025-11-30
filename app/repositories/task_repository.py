from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.task import Task

class TaskRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, task: Task) -> Task:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_by_id(self, task_id: int) -> Optional[Task]:
        return self.db.query(Task).filter(Task.id == task_id).first()

    def get_by_project(self, project_id: int) -> List[Task]:
        return (
            self.db.query(Task)
            .filter(Task.project_id == project_id)
            .order_by(Task.created_at.desc())
            .all()
        )

    def update(self, task: Task) -> Task:
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task_id: int) -> bool:
        task = self.get_by_id(task_id)
        if task:
            self.db.delete(task)
            self.db.commit()
            return True
        return False

    def count_by_project(self, project_id: int) -> int:
        return self.db.query(Task).filter(Task.project_id == project_id).count()

    def get_overdue_tasks(self) -> List[Task]:
        from datetime import datetime
        return (
            self.db.query(Task)
            .filter(Task.deadline < datetime.now(), Task.status != "done")
            .all()
        )
