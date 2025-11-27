class RepositoryException(Exception):
    """Base exception for repository layer"""
    pass

class ProjectNotFoundException(RepositoryException):
    def __init__(self, project_id: int):
        self.project_id = project_id
        super().__init__(f"❌ Project with ID {project_id} not found!")

class TaskNotFoundException(RepositoryException):
    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"❌ Task with ID {task_id} not found!")

class DuplicateProjectNameException(RepositoryException):
    def __init__(self, project_name: str):
        self.project_name = project_name
        super().__init__(f"❌ Project name '{project_name}' already exists!")