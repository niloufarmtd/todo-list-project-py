from app.db.session import SessionLocal
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.services.project_service import ProjectService
from app.services.task_service import TaskService
from app.exceptions.service_exceptions import (
    ProjectLimitExceededException,
    TaskLimitExceededException,
    InvalidTaskStatusException,
    PastDeadlineException,
    ProjectNotFoundException,
    TaskNotFoundException,
    DuplicateProjectNameException
)
from datetime import datetime
import os

def display_menu():
    """Display the main menu"""
    print("\n📝 ToDo List Manager (PostgreSQL)")
    print("1. Create new project")
    print("2. Show all projects")
    print("3. Add task to project")
    print("4. Show tasks of a project")
    print("5. Edit project")
    print("6. Delete project")
    print("7. Delete task")
    print("8. Change task status")
    print("9. Edit task")
    print("10. Exit")

def get_db_session():
    """Get database session"""
    return SessionLocal()

def main():
    db = get_db_session()
    
    try:
        # Initialize repositories and services
        project_repo = ProjectRepository(db)
        task_repo = TaskRepository(db)
        project_service = ProjectService(project_repo, task_repo)
        task_service = TaskService(task_repo)

        while True:
            display_menu()
            choice = input("Please enter your choice (1-10): ")

            if choice == "1":
                # Create new project
                name = input("Project name: ")
                description = input("Project description: ")
                try:
                    project = project_service.create_project(name, description)
                    print("✅ Project created successfully!")
                except Exception as e:
                    print(f"❌ {e}")

            elif choice == "2":
                # Show all projects
                try:
                    projects = project_service.get_all_projects()
                    if not projects:
                        print("📭 No projects found")
                    else:
                        print("\n Your Projects (newest first):")
                        for project in projects:
                            task_count = project_service.get_task_count(project.id)
                            created_str = project.created_at.strftime("%Y-%m-%d %H:%M")
                            
                            if task_count == 0:
                                task_display = "No tasks"
                            else:
                                task_display = f"{task_count} task{'s' if task_count > 1 else ''}"
                            
                            print(f"   {project.id}. {project.name} - {project.description}")
                            print(f"      {task_display} | Created: {created_str}")
                except Exception as e:
                    print(f"❌ {e}")

            elif choice == "3":
                # Add task to project
                try:
                    project_id = int(input("Project ID: "))
                    title = input("Task title: ")
                    description = input("Task description: ")
                    deadline_input = input("Deadline (YYYY-MM-DD) or press Enter for no deadline: ")
                    
                    deadline = None
                    if deadline_input.strip():
                        deadline = task_service.validate_deadline(deadline_input)
                    
                    task = project_service.add_task_to_project(project_id, title, description, deadline)
                    print("✅ Task created successfully!")
                except Exception as e:
                    print(f"❌ {e}")

            elif choice == "4":
                # Show tasks of a project
                try:
                    project_id = int(input("Project ID: "))
                    tasks = task_repo.get_by_project(project_id)
                    if not tasks:
                        print("📭 No tasks found for this project")
                    else:
                        print(f"\n📋 Tasks for Project {project_id}:")
                        for task in tasks:
                            deadline_str = task.deadline.strftime("%Y-%m-%d") if task.deadline else "No deadline"
                            status_icon = "🔴" if task.status == "todo" else "🟡" if task.status == "doing" else "🟢"
                            print(f"   {task.id}. {task.title} - Status: {status_icon} {task.status} - Deadline: {deadline_str}")
                except Exception as e:
                    print(f"❌ {e}")

            elif choice == "5":
                # Edit project
                try:
                    project_id = int(input("Project ID to edit: "))
                    new_name = input("New project name: ")
                    new_description = input("New project description: ")
                    project = project_service.update_project(project_id, new_name, new_description)
                    print("✅ Project updated successfully!")
                except Exception as e:
                    print(f"❌ {e}")

            elif choice == "6":
                # Delete project
                try:
                    project_id = int(input("Project ID to delete: "))
                    confirm = input("Are you sure? This will delete ALL tasks in this project! (y/n): ")
                    if confirm.lower() == 'y':
                        tasks = task_repo.get_by_project(project_id)
                        if tasks:
                            print(f"  This will delete {len(tasks)} tasks:")
                            for task in tasks:
                                print(f"   - {task.title}")
                        
                        confirm_final = input("Type 'DELETE' to confirm: ")
                        if confirm_final == 'DELETE':
                            project_service.delete_project(project_id)
                            print("✅ Project and all its tasks deleted successfully!")
                        else:
                            print("❌ Deletion cancelled")
                    else:
                        print("❌ Deletion cancelled")
                except Exception as e:
                    print(f"❌ {e}")

            elif choice == "7":
                # Delete task
                try:
                    task_id = int(input("Task ID to delete: "))
                    task_service.delete_task(task_id)
                    print("✅ Task deleted successfully!")
                except Exception as e:
                    print(f"❌ {e}")

            elif choice == "8":
                # Change task status
                try:
                    task_id = int(input("Task ID: "))
                    print("Status options: todo, doing, done")
                    new_status = input("New status: ")
                    task_service.change_task_status(task_id, new_status)
                    print(f"✅ Task status changed to {new_status}")
                except Exception as e:
                    print(f"❌ {e}")

            elif choice == "9":
                # Edit task
                try:
                    task_id = int(input("Task ID to edit: "))
                    new_title = input("New title: ")
                    new_description = input("New description: ")
                    print("Status options: todo, doing, done")
                    new_status = input("New status: ")
                    new_deadline_input = input("New deadline (YYYY-MM-DD) or press Enter: ")
                    
                    new_deadline = None
                    if new_deadline_input.strip():
                        new_deadline = task_service.validate_deadline(new_deadline_input)
                    
                    # First get the task
                    task = task_repo.get_by_id(task_id)
                    if not task:
                        raise TaskNotFoundException(task_id)
                    
                    # Update task
                    task.title = new_title
                    task.description = new_description
                    task.status = new_status
                    task.deadline = new_deadline
                    
                    if new_status == "done" and not task.closed_at:
                        task.closed_at = datetime.now()
                    
                    task_repo.update(task)
                    print("✅ Task updated successfully!")
                except Exception as e:
                    print(f"❌ {e}")
            
            elif choice == "10":
                # Exit
                print("👋 Goodbye!")
                break

            else:
                print("❌ Invalid choice. Please enter a number between 1-10")

    finally:
        db.close()

if __name__ == "__main__":
    main()