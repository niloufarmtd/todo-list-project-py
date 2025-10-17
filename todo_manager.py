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
    

      def create_project(self, name: str, description: str) -> tuple[bool, str]:
    """
    Create a new project with validation
    
    Args:
        name (str): Project name (maximum 30 characters)
        description (str): Project description (maximum 150 characters)
    
    Returns:
        tuple[bool, str]: (success status, message)
    """
    # Validate name length
    if len(name) > 30:
        return False, "❌ Project name is too long! Maximum 30 characters allowed."
    
    # Validate description length  
    if len(description) > 150:
        return False, "❌ Project description is too long! Maximum 150 characters allowed."
    
    # Check maximum projects limit
    if len(self.storage.projects) >= self.max_projects:
        return False, f"❌ Maximum projects limit reached! You can only have {self.max_projects} projects."
    
    # Check for duplicate project names
    for project in self.storage.projects:
        if project.name == name:
            return False, "❌ Project name already exists! Please choose a different name."
    
    # Create and save the project
    project = Project(None, name, description)
    self.storage.add_project(project)
    return True, "✅ Project created successfully!"

    from datetime import datetime

    def add_task(self, project_id: int, title: str, description: str, deadline_str: str = None) -> tuple[bool, str]:
    """
    Add a new task to a project with validation
    
    Args:
        project_id (int): ID of the project to add the task to
        title (str): Task title (maximum 30 characters)
        description (str): Task description (maximum 150 characters)
        deadline_str (str, optional): Deadline in YYYY-MM-DD format
    
    Returns:
        tuple[bool, str]: (success status, message)
    """
    # Validate title length
    if len(title) > 30:
        return False, "❌ Task title is too long! Maximum 30 characters allowed."
    
    # Validate description length
    if len(description) > 150:
        return False, "❌ Task description is too long! Maximum 150 characters allowed."
    
    # Validate and parse deadline
    deadline = None
    if deadline_str:
        try:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
            # Check if deadline is in the future
            if deadline < datetime.now():
                return False, "❌ Deadline cannot be in the past! Please enter a future date."
        except ValueError:
            return False, "❌ Invalid date format! Please use YYYY-MM-DD (e.g., 2024-12-31)"
    
    # Check if project exists
    project_exists = any(p.id == project_id for p in self.storage.projects)
    if not project_exists:
        return False, "❌ Project not found! Please check the Project ID."
    
    # Check maximum tasks limit for this project
    project_tasks = self.storage.get_tasks_by_project(project_id)
    if len(project_tasks) >= self.max_tasks:
        return False, f"❌ Task limit reached! Each project can have maximum {self.max_tasks} tasks."
    
    # Create and save the task
    task = Task(None, title, description, project_id, deadline)
    self.storage.add_task(task)
    return True, "✅ Task created successfully!"
    
    def edit_project(self, project_id: int, new_name: str, new_description: str) -> tuple[bool, str]:
    """
    Edit an existing project
    
    Args:
        project_id (int): ID of the project to edit
        new_name (str): New project name (maximum 30 characters)
        new_description (str): New project description (maximum 150 characters)
    
    Returns:
        tuple[bool, str]: (success status, message)
    """
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
            return False, "❌ Project not found! Please check the Project ID."

        # Check for duplicate name (excluding current project)
        for p in self.storage.projects:
            if p.id != project_id and p.name == new_name:
                return False, "❌ Project name already exists! Please choose a different name."

        # Update project
        project.name = new_name
        project.description = new_description
                  return True, "Project updated successfully"
    

     def edit_task(self, task_id: int, new_title: str, new_description: str, new_status: str, new_deadline_str: str = None) -> tuple[bool, str]:
    """
    Edit task details
    
    Args:
        task_id (int): ID of the task to edit
        new_title (str): New task title (maximum 30 characters)
        new_description (str): New task description (maximum 150 characters)
        new_status (str): New task status (must be: todo, doing, or done)
        new_deadline_str (str, optional): New deadline in YYYY-MM-DD format
    
    Returns:
        tuple[bool, str]: (success status, message)
    """
        # Validate title length
        if len(new_title) > 30:
            return False, "Task title cannot exceed 30 characters"

        # Validate description length
        if len(new_description) > 150:
            return False, "Task description cannot exceed 150 characters"

        # Validate status
        valid_statuses = ["todo", "doing", "done"]
        if new_status not in valid_statuses:
            return False, "❌ Invalid status! Please choose from: 'todo', 'doing', or 'done'"

        # Validate and parse deadline
        new_deadline = None
        if new_deadline_str:
            try:
                new_deadline = datetime.strptime(new_deadline_str, "%Y-%m-%d")
                if new_deadline < datetime.now():
                     return False, "❌ Deadline cannot be in the past! Please enter a future date."
            except ValueError:
                return False, "❌ Invalid date format! Please use YYYY-MM-DD (e.g., 2024-12-31)"

        # Find the task
        task = None
        for t in self.storage.tasks:
            if t.id == task_id:
                task = t
                break

        if not task:
            return False, "❌ Task not found! Please check the Task ID."

        # Update task
        task.title = new_title
        task.description = new_description
        task.status = new_status
        task.deadline = new_deadline

        return True, "Task updated successfully"

 def delete_project(self, project_id: int) -> tuple[bool, str]:
    """
    Delete a project and all its tasks (Cascade Delete)
    
    Args:
        project_id (int): ID of the project to delete
    
    Returns:
        tuple[bool, str]: (success status, message)
    """
        # Find the project
        project_exists = any(p.id == project_id for p in self.storage.projects)

    if not project_exists:
        return False, "❌ Project not found! Please check the Project ID."

        # Delete the project and all its tasks
        self.storage.delete_project(project_id)
        return True, "Project and all its tasks deleted successfully"

    
     def delete_task(self, task_id: int) -> tuple[bool, str]:
    """
    Delete a specific task
    
    Args:
        task_id (int): ID of the task to delete
    
    Returns:
        tuple[bool, str]: (success status, message)
    """
        # Find the task
        task_exists = any(t.id == task_id for t in self.storage.tasks)

        if not task_exists:
             return False, "❌ Task not found! Please check the Task ID."

        # Delete the task
        self.storage.delete_task(task_id)
        return True, "Task deleted successfully"

    def change_task_status(self, task_id: int, new_status: str) -> tuple[bool, str]:
    """
    Change task status (todo/doing/done)
    
    Args:
        task_id (int): ID of the task to update
        new_status (str): New status (must be: todo, doing, or done)
    
    Returns:
        tuple[bool, str]: (success status, message)
    """
        # Validate status
        valid_statuses = ["todo", "doing", "done"]
        if new_status not in valid_statuses:
           return False, "❌ Invalid status! Please choose from: 'todo', 'doing', or 'done'"

        # Find the task
        task = None
        for t in self.storage.tasks:
            if t.id == task_id:
                task = t
                break

        if not task:
            return False, "❌ Task not found! Please check the Task ID."

        # Update status
        task.status = new_status
        return True, f"Task status changed to {new_status}"

    def change_task_status(self, task_id: int, new_status: str) -> tuple[bool, str]:
    """
    Change task status (todo/doing/done)
    
    Args:
        task_id (int): ID of the task to update
        new_status (str): New status (must be: todo, doing, or done)
    
    Returns:
        tuple[bool, str]: (success status, message)
    """
        return sorted(self.storage.projects, key=lambda x: x.created_at, reverse=True)

    def list_tasks(self, project_id: int) -> list:
    """
    Get all tasks for a specific project
    
    Args:
        project_id (int): ID of the project
    
    Returns:
        list: List of Task objects for the specified project
    """
        return self.storage.get_tasks_by_project(project_id)


     def get_task_count(self, project_id: int) -> int:
    """
    Get the number of tasks in a specific project
    
    Args:
        project_id (int): ID of the project
    
    Returns:
        int: Number of tasks in the project
    """
    tasks = self.storage.get_tasks_by_project(project_id)
    return len(tasks)
