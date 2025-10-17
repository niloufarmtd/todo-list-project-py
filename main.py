from todo_manager import TodoManager


def display_menu():
    """Display the main menu"""
    print("\n📝 ToDo List Manager")
    print("1. Create new project")
    print("2. Show all projects")
    print("3. Add task to project")
    print("4. Show tasks of a project")
    print("5. Edit project")
    print("6. Delete task")
    print("7. Change task status")
    print("8. Edit task")
    print("9. Exit")


def main():
    """Main function to run the application"""
    manager = TodoManager()

    while True:
        display_menu()
        choice = input("Please enter your choice (1-9): ")

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
                print("\n📂 Your Projects:")
                for project in projects:
                    print(f"   {project.id}. {project.name} - {project.description}")

        elif choice == "3":
            # Add task to project
            try:
                project_id = int(input("Project ID: "))
                title = input("Task title: ")
                description = input("Task description: ")
                
                print("✅" if success else "❌", message)
            except ValueError:
                print("❌ Please enter a valid number for Project ID")
    
                deadline_input = input("Deadline (YYYY-MM-DD) or press Enter for no deadline: ")

                deadline_str = deadline_input if deadline_input.strip() else None

                success, message = manager.add_task(project_id, title, description, deadline_str)

        
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
            # Delete task
            try:
                task_id = int(input("Task ID to delete: "))
                success, message = manager.delete_task(task_id)
                print("✅" if success else "❌", message)
            except ValueError:
                print("❌ Please enter a valid number for Task ID")

        elif choice == "7":
            # Change task status
            try:
                task_id = int(input("Task ID: "))
                print("Status options: todo, doing, done")
                new_status = input("New status: ")
                success, message = manager.change_task_status(task_id, new_status)
                print("✅" if success else "❌", message)
            except ValueError:
                print("❌ Please enter a valid number for Task ID")

        elif choice == "8":

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
        
        elif choice == "9":
            # Exit
            print("Goodbye!")
            break

        else:
            # Exit
            print("Goodbye!")
            break

        else:
            print("❌ Invalid choice. Please enter a number between 1-9")
8

if __name__ == "__main__":
    main()
