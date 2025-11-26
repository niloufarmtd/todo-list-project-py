from .repository_exceptions import ProjectNotFoundException, TaskNotFoundException, DuplicateProjectNameException

class ServiceException(Exception):
    """Base exception for service layer"""
    pass

class ProjectLimitExceededException(ServiceException):
    def __init__(self, max_projects: int):
        self.max_projects = max_projects
        super().__init__(f"❌ Maximum projects limit reached! You can only have {max_projects} projects.")

class TaskLimitExceededException(ServiceException):
    def __init__(self, max_tasks: int):
        self.max_tasks = max_tasks
        super().__init__(f"❌ Task limit reached! Each project can have maximum {max_tasks} tasks.")

class InvalidTaskStatusException(ServiceException):
    def __init__(self, status: str):
        self.status = status
        super().__init__(f"❌ Invalid status '{status}'! Please choose from: 'todo', 'doing', or 'done'")

class PastDeadlineException(ServiceException):
    def __init__(self):
        super().__init__("❌ Deadline cannot be in the past! Please enter a future date.")

# Re-export repository exceptions for service layer use
__all__ = [
    'ServiceException',
    'ProjectLimitExceededException', 
    'TaskLimitExceededException',
    'InvalidTaskStatusException',
    'PastDeadlineException',
    'ProjectNotFoundException',
    'TaskNotFoundException',
    'DuplicateProjectNameException'
]