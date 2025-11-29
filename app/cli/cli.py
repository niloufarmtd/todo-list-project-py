from app.db.session import SessionLocal
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.models.project import Project
from app.models.task import Task
from datetime import datetime

def create_project_cli():
    name = input("Project name: ")
    description = input("Project description: ")

    db = SessionLocal()
    repo = ProjectRepository(db)

    project = Project(name=name, description=description)
    repo.create(project)

    print("✅ Project created with ID:", project.id)
    db.close()

def list_projects_cli():
    db = SessionLocal()
    repo = ProjectRepository(db)

    projects = repo.get_all()
    print("\n📌 Projects:")
    for p in projects:
        print(f"- [{p.id}] {p.name} | {p.description}")

    db.close()

def create_task_cli():
    project_id = int(input("Project ID: "))
    title = input("Task title: ")
    description = input("Task description: ")

    deadline_str = input("Deadline (YYYY-MM-DD) or press Enter: ")
    deadline = None

    if deadline_str.strip():
        try:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
        except ValueError:
            print("❌ Invalid deadline format")
            return

    db = SessionLocal()
    repo = TaskRepository(db)

    task = Task(
        title=title,
        description=description,
        project_id=project_id,
        deadline=deadline
    )

    repo.create(task)

    print("✅ Task created with ID:", task.id)
    db.close()

def list_tasks_cli():
    project_id = int(input("Project ID: "))

    db = SessionLocal()
    repo = TaskRepository(db)

    tasks = repo.get_by_project(project_id)

    print("\n📝 Tasks:")
    for t in tasks:
        print(f"- [{t.id}] {t.title} | status: {t.status} | deadline: {t.deadline}")

    db.close()

def delete_task_cli():
    task_id = int(input("Task ID to delete: "))

    db = SessionLocal()
    repo = TaskRepository(db)

    ok = repo.delete(task_id)
    if ok:
        print("🗑 Task deleted.")
    else:
        print("❌ Task not found.")

    db.close()

def main_menu():
    while True:
        print("\n=== Todo CLI ===")
        print("1. Create project")
        print("2. List projects")
        print("3. Create task")
        print("4. List tasks in project")
        print("5. Delete task")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            create_project_cli()
        elif choice == "2":
            list_projects_cli()
        elif choice == "3":
            create_task_cli()
        elif choice == "4":
            list_tasks_cli()
        elif choice == "5":
            delete_task_cli()
        elif choice == "0":
            break
        else:
            print("❌ Invalid option")


if __name__ == "__main__":
    main_menu()
