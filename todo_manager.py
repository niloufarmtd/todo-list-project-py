import os
from dotenv import load_dotenv
from models import Project, Task
from storage import InMemoryStorage

# Load environment variables from .env file
load_dotenv()

class TodoManager:
    """Main business logic for Todo List application"""
    
    def __init__(self):
        self.storage = InMemoryStorage()
        # Get limits from environment variables or use defaults
        self.max_projects = int(os.getenv("MAX_NUMBER_OF_PROJECTS", 10))
        self.max_tasks = int(os.getenv("MAX_NUMBER_OF_TASKS_PER_PROJECT", 50))
    
    def create_project(self, name, description):
        """Create a new project with validation"""
        # Check maximum projects limit
        if len(self.storage.projects) >= self.max_projects:
            return False, f"Cannot have more than {self.max_projects} projects"
        
        # Check for duplicate project names
        for project in self.storage.projects:
            if project.name == name:
                return False, "Project name already exists"
        
        # Create and save the project
        project = Project(None, name, description)
        self.storage.add_project(project)
        return True, "Project created successfully"
    
    def add_task(self, project_id, title, description):
        """Add a new task to a project with validation"""
        # Check if project exists
        project_exists = any(p.id == project_id for p in self.storage.projects)
        if not project_exists:
            return False, "Project does not exist"
        
        # Check maximum tasks limit for this project
        project_tasks = self.storage.get_tasks_by_project(project_id)
        if len(project_tasks) >= self.max_tasks:
            return False, f"Cannot have more than {self.max_tasks} tasks in a project"
        
        # Create and save the task
        task = Task(None, title, description, project_id)
        self.storage.add_task(task)
        return True, "Task created successfully"
    
    def list_projects(self):
        """Get all projects"""
        return self.storage.get_all_projects()
    
    def list_tasks(self, project_id):
        """Get all tasks for a specific project"""
        return self.storage.get_tasks_by_project(project_id)
