from todo_manager import TodoManager


def display_menu():
    """Display the main menu"""
    print("\n📝 ToDo List Manager")
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

def main():
    storage = InMemoryStorage()
    manager = TodoManager(storage)

    while True:
        display_menu()
        choice = input("Please enter your choice (1-10): ")

        if choice == "1":
            # Create new project
            name = input("Project name: ")
            description = input("Project description: ")
            success, message = manager.create_project(name, description)
            print("✅" if success else "❌", message)

        elif choice == "2":
            # Show all projects
            projects = manager.list_projects()
            if not projects:
                print("📭 No projects found")
            else:
                print("\n Your Projects (newest first):")
                for project in projects:
                    # Get task count for this project
                    task_count = manager.get_task_count(project.id)
                    created_str = project.created_at.strftime("%Y-%m-%d %H:%M")
                    
                    # Display project with task count
                    if task_count == 0:
                        task_display = "No tasks"
                    else:
                        task_display = f"{task_count} task{'s' if task_count > 1 else ''}"
                    
                    print(f"   {project.id}. {project.name} - {project.description}")
                    print(f"      {task_display} |  Created: {created_str}")

        elif choice == "3":
            # Add task to project
            try:
                project_id = int(input("Project ID: "))
                title = input("Task title: ")
                description = input("Task description: ")
                deadline_input = input("Deadline (YYYY-MM-DD) or press Enter for no deadline: ")
                deadline_str = deadline_input if deadline_input.strip() else None
                success, message = manager.add_task(project_id, title, description, deadline_str)
                print("✅" if success else "❌", message)
            except ValueError:
                print("❌ Please enter a valid number for Project ID")

        elif choice == "4":
            # Show tasks of a project
            try:
                project_id = int(input("Project ID: "))
                tasks = manager.list_tasks(project_id)
                if not tasks:
                    print("📭 No tasks found for this project")
                else:
                    print(f"\n📋 Tasks for Project {project_id}:")
                    for task in tasks:
                        deadline_str = task.deadline.strftime("%Y-%m-%d") if task.deadline else "No deadline"
                        print(f"   {task.id}. {task.title} - Status: {task.status} - Deadline: {deadline_str}")
            except ValueError:
                print("❌ Please enter a valid number for Project ID")

        elif choice == "5":
            # Edit project
            try:
                project_id = int(input("Project ID to edit: "))
                new_name = input("New project name: ")
                new_description = input("New project description: ")
                success, message = manager.edit_project(project_id, new_name, new_description)
                print("✅" if success else "❌", message)
            except ValueError:
                print("❌ Please enter a valid number for Project ID")

        elif choice == "6":
            # Delete project
            try:
                project_id = int(input("Project ID to delete: "))
                # Confirm deletion
                confirm = input("Are you sure? This will delete ALL tasks in this project! (y/n): ")
                if confirm.lower() == 'y':
                    # First, let's show what will be deleted
                    tasks = manager.list_tasks(project_id)
                    if tasks:
                        print(f"  This will delete {len(tasks)} tasks:")
                        for task in tasks:
                            print(f"   - {task.title}")
                    
                    confirm_final = input("Type 'DELETE' to confirm: ")
                    if confirm_final == 'DELETE':
                        success, message = manager.delete_project(project_id)
                        print("✅" if success else "❌", message)
                    else:
                        print("❌ Deletion cancelled")
                else:
                    print("❌ Deletion cancelled")
            except ValueError:
                print("❌ Please enter a valid number for Project ID")

        elif choice == "7":
            # Delete task
            try:
                task_id = int(input("Task ID to delete: "))
                success, message = manager.delete_task(task_id)
                print("✅" if success else "❌", message)
            except ValueError:
                print("❌ Please enter a valid number for Task ID")

        elif choice == "8":
            # Change task status
            try:
                task_id = int(input("Task ID: "))
                print("Status options: todo, doing, done")
                new_status = input("New status: ")
                success, message = manager.change_task_status(task_id, new_status)
                print("✅" if success else "❌", message)
            except ValueError:
                print("❌ Please enter a valid number for Task ID")

        elif choice == "9":
            # Edit task
            try:
                task_id = int(input("Task ID to edit: "))
                new_title = input("New title: ")
                new_description = input("New description: ")
                print("Status options: todo, doing, done")
                new_status = input("New status: ")
                new_deadline = input("New deadline (YYYY-MM-DD) or press Enter: ")
                new_deadline_str = new_deadline if new_deadline.strip() else None
                success, message = manager.edit_task(task_id, new_title, new_description, new_status, new_deadline_str)
                print("✅" if success else "❌", message)
            except ValueError:
                print("❌ Please enter a valid number for Task ID")
        
        elif choice == "10":
            # Exit
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid choice. Please enter a number between 1-10")


if __name__ == "__main__":
    main()