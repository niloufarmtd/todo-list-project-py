from todo_manager import TodoManager

def display_menu():
    """Display the main menu"""
    print("\n📝 ToDo List Manager")
    print("1. Create new project")
    print("2. Show all projects")
    print("3. Add task to project")
    print("4. Show tasks of a project")
    print("5. Exit")

def main():
    """Main function to run the application"""
    manager = TodoManager()
    
    while True:
        display_menu()
        choice = input("Please enter your choice (1-5): ")
        
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
                success, message = manager.add_task(project_id, title, description)
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
                        print(f"   {task.id}. {task.title} - Status: {task.status}")
            except ValueError:
                print("❌ Please enter a valid number for Project ID")
        
        elif choice == "5":
            # Exit
            print("Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please enter a number between 1-5")

if __name__ == "__main__":
    main()
