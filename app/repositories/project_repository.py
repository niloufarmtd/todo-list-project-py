from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.project import Project
from app.db.session import get_db

class ProjectRepository:
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, project: Project) -> Project:
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project
    
    def get_by_id(self, project_id: int) -> Optional[Project]:
        return self.db.query(Project).filter(Project.id == project_id).first()
    
    def get_all(self) -> List[Project]:
        return self.db.query(Project).order_by(Project.created_at.desc()).all()
    
    def get_by_name(self, name: str) -> Optional[Project]:
        return self.db.query(Project).filter(Project.name == name).first()
    
    def update(self, project: Project) -> Project:
        self.db.commit()
        self.db.refresh(project)
        return project
    
    def delete(self, project_id: int) -> bool:
        project = self.get_by_id(project_id)
        if project:
            self.db.delete(project)
            self.db.commit()
            return True
        return False
    
    def count(self) -> int:
        return self.db.query(Project).count()