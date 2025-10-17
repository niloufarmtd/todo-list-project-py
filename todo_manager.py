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
    # Validate name length
    if len(name) > 30:
        return False, "Project name cannot exceed 30 characters"
    
    # Validate description length  
    if len(description) > 150:
        return False, "Project description cannot exceed 150 characters"
    
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
    # Validate title length
    if len(title) > 30:
        return False, "Task title cannot exceed 30 characters"
    
    # Validate description length
    if len(description) > 150:
        return False, "Task description cannot exceed 150 characters"
    
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

       def edit_project(self, project_id, new_name, new_description):
    """Edit an existing project"""
    # Validate name length
    if len(new_name) > 30:
        return False, "Project name cannot exceed 30 characters"
    
    # Validate description length
    if len(new_description) > 150:
        return False, "Project description cannot exceed 150 characters"
    
    # Find the project
    project = None
    for p in self.storage.projects:
        if p.id == project_id:
            project = p
            break
    
    if not project:
        return False, "Project not found"
    
    # Check for duplicate name (excluding current project)
    for p in self.storage.projects:
        if p.id != project_id and p.name == new_name:
            return False, "Project name already exists"

    # Update project
    project.name = new_name
    project.description = new_description
    return True, "Project updated successfully"

    
    def delete_task(self, task_id):
    """Delete a specific task"""
    # Find the task
    task_exists = any(t.id == task_id for t in self.storage.tasks)
    
    if not task_exists:
        return False, "Task not found"
    
    # Delete the task
    self.storage.delete_task(task_id)
    return True, "Task deleted successfully"
       
    def list_projects(self):
        """Get all projects"""
        return self.storage.get_all_projects()
    
    def list_tasks(self, project_id):
        """Get all tasks for a specific project"""
        return self.storage.get_tasks_by_project(project_id)
