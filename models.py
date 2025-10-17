from datetime import datetime


class Project:
    """Model for representing a project"""

    def __init__(self, id: int, name: str, description: str):
        """
        Initialize a new Project

        Args:
            id (int): Project ID (use None for new projects)
            name (str): Project name
            description (str): Project description
        """
        self.id = id
        self.name = name
        self.description = description
        self.created_at = datetime.now()

    def __str__(self) -> str:
        """String representation of the project"""
        return f"Project {self.id}: {self.name}"


class Task:
    """Model for representing a task"""

    def __init__(self, id: int, title: str, description: str, project_id: int, deadline: datetime = None):
        """
        Initialize a new Task

        Args:
            id (int): Task ID (use None for new tasks)
            title (str): Task title
            description (str): Task description
            project_id (int): ID of the parent project
            deadline (datetime, optional): Task deadline
        """
        self.id = id
        self.title = title
        self.description = description
        self.status = "todo"  # default status
        self.project_id = project_id
        self.deadline = deadline
        self.created_at = datetime.now()

    def __str__(self) -> str:
        """String representation of the task"""
        deadline_str = self.deadline.strftime("%Y-%m-%d") if self.deadline else "No deadline"
        return f"Task {self.id}: {self.title} ({self.status}) - Deadline: {deadline_str}"
