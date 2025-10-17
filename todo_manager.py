import os
from datetime import datetime
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

    from datetime import datetime

    def add_task(self, project_id, title, description, deadline_str=None):
        """Add a new task to a project with validation"""
        # Validate title length
        if len(title) > 30:
            return False, "Task title cannot exceed 30 characters"

        # Validate description length
        if len(description) > 150:
            return False, "Task description cannot exceed 150 characters"

        # Validate and parse deadline
        deadline = None
        if deadline_str:
            try:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
                # Check if deadline is in the future
                if deadline < datetime.now():
                    return False, "Deadline cannot be in the past"
            except ValueError:
                return False, "Invalid deadline format. Use YYYY-MM-DD"

        # Check if project exists
        project_exists = any(p.id == project_id for p in self.storage.projects)
        if not project_exists:
            return False, "Project does not exist"

        # Check maximum tasks limit for this project
        project_tasks = self.storage.get_tasks_by_project(project_id)
        if len(project_tasks) >= self.max_tasks:
            return False, f"Cannot have more than {self.max_tasks} tasks in a project"

        # Create and save the task
        task = Task(None, title, description, project_id, deadline)
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
    

    def edit_task(self, task_id, new_title, new_description, new_status, new_deadline_str=None):
        """Edit task details"""
        # Validate title length
        if len(new_title) > 30:
            return False, "Task title cannot exceed 30 characters"

        # Validate description length
        if len(new_description) > 150:
            return False, "Task description cannot exceed 150 characters"

        # Validate status
        valid_statuses = ["todo", "doing", "done"]
        if new_status not in valid_statuses:
            return False, "Invalid status. Must be: todo, doing, or done"

        # Validate and parse deadline
        new_deadline = None
        if new_deadline_str:
            try:
                new_deadline = datetime.strptime(new_deadline_str, "%Y-%m-%d")
                if new_deadline < datetime.now():
                    return False, "Deadline cannot be in the past"
            except ValueError:
                return False, "Invalid deadline format. Use YYYY-MM-DD"

        # Find the task
        task = None
        for t in self.storage.tasks:
            if t.id == task_id:
                task = t
                break

        if not task:
            return False, "Task not found"

        # Update task
        task.title = new_title
        task.description = new_description
        task.status = new_status
        task.deadline = new_deadline

        return True, "Task updated successfully"

    def delete_task(self, task_id):
        """Delete a specific task"""
        # Find the task
        task_exists = any(t.id == task_id for t in self.storage.tasks)

        if not task_exists:
            return False, "Task not found"

        # Delete the task
        self.storage.delete_task(task_id)
        return True, "Task deleted successfully"

    def change_task_status(self, task_id, new_status):
        """Change task status (todo/doing/done)"""
        # Validate status
        valid_statuses = ["todo", "doing", "done"]
        if new_status not in valid_statuses:
            return False, "Invalid status. Must be: todo, doing, or done"

        # Find the task
        task = None
        for t in self.storage.tasks:
            if t.id == task_id:
                task = t
                break

        if not task:
            return False, "Task not found"

        # Update status
        task.status = new_status
        return True, f"Task status changed to {new_status}"

    def list_projects(self):
        """Get all projects sorted by creation time (newest first)"""
        return sorted(self.storage.projects, key=lambda x: x.created_at, reverse=True)

    def list_tasks(self, project_id):
        """Get all tasks for a specific project"""
        return self.storage.get_tasks_by_project(project_id)
