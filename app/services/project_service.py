from datetime import datetime
from app.exceptions.service_exceptions import (
    ProjectLimitExceededException,
    TaskLimitExceededException,
    ProjectNotFoundException,
    DuplicateProjectNameException
)
from app.models.project import Project
from app.models.task import Task
import os

class ProjectService:
    def __init__(self, project_repository, task_repository):
        self.project_repo = project_repository
        self.task_repo = task_repository
        self.max_projects = int(os.getenv("MAX_NUMBER_OF_PROJECTS", 10))
        self.max_tasks = int(os.getenv("MAX_NUMBER_OF_TASKS_PER_PROJECT", 50))

    def create_project(self, name: str, description: str) -> Project:
        if len(name) > 30:
            raise ValueError("❌ Project name is too long! Maximum 30 characters allowed.")

        if len(description) > 150:
            raise ValueError("❌ Project description is too long! Maximum 150 characters allowed.")

        project_count = self.project_repo.count()
        if project_count >= self.max_projects:
            raise ProjectLimitExceededException(self.max_projects)

        existing_project = self.project_repo.get_by_name(name)
        if existing_project:
            raise DuplicateProjectNameException(name)

        project = Project(name=name, description=description)
        return self.project_repo.create(project)

    def add_task_to_project(self, project_id: int, title: str, description: str, deadline=None):
        if len(title) > 30:
            raise ValueError("❌ Task title is too long! Maximum 30 characters allowed.")

        if len(description) > 150:
            raise ValueError("❌ Task description is too long! Maximum 150 characters allowed.")

        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundException(project_id)

        task_count = self.task_repo.count_by_project(project_id)
        if task_count >= self.max_tasks:
            raise TaskLimitExceededException(self.max_tasks)

        task = Task(
            title=title,
            description=description,
            project_id=project_id,
            deadline=deadline
        )

        return self.task_repo.create(task)

    def get_all_projects(self):
        return self.project_repo.get_all()

    def get_project_by_id(self, project_id: int) -> Project:
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundException(project_id)
        return project

    def update_project(self, project_id: int, new_name: str, new_description: str) -> Project:
        if len(new_name) > 30:
            raise ValueError("❌ Project name is too long! Maximum 30 characters allowed.")

        if len(new_description) > 150:
            raise ValueError("❌ Project description is too long! Maximum 150 characters allowed.")

        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundException(project_id)

        existing_project = self.project_repo.get_by_name(new_name)
        if existing_project and existing_project.id != project_id:
            raise DuplicateProjectNameException(new_name)

        project.name = new_name
        project.description = new_description
        return self.project_repo.update(project)

    def delete_project(self, project_id: int):
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundException(project_id)
        
        return self.project_repo.delete(project_id)

    def get_task_count(self, project_id: int) -> int:
        return self.task_repo.count_by_project(project_id)
