from models import Project, Task


class InMemoryStorage:
    """In-memory storage for projects and tasks"""

    def __init__(self):
        """Initialize in-memory storage with empty lists and ID counters"""
        self.projects = []
        self.tasks = []
        self.next_project_id = 1
        self.next_task_id = 1

    def add_project(self, project: Project) -> Project:
        """
        Add a new project and assign auto-increment ID

        Args:
            project (Project): Project object to add

        Returns:
            Project: The added project with assigned ID
        """
        project.id = self.next_project_id
        self.next_project_id += 1
        self.projects.append(project)
        return project

    def add_task(self, task: Task) -> Task:
        """
        Add a new task and assign auto-increment ID

        Args:
            task (Task): Task object to add

        Returns:
            Task: The added task with assigned ID
        """
        task.id = self.next_task_id
        self.next_task_id += 1
        self.tasks.append(task)
        return task

    def get_all_projects(self) -> list:
        """
        Get all projects

        Returns:
            list: List of all Project objects
        """
        return self.projects

    def get_tasks_by_project(self, project_id: int) -> list:
        """
        Get all tasks for a specific project sorted by creation time

        Args:
            project_id (int): ID of the project

        Returns:
            list: List of Task objects for the specified project (newest first)
        """
        tasks = [task for task in self.tasks if task.project_id == project_id]
        return sorted(tasks, key=lambda x: x.created_at, reverse=True)

    def delete_project(self, project_id: int) -> None:
        """
        Delete a project and all its tasks (Cascade Delete)

        Args:
            project_id (int): ID of the project to delete
        """
        # Remove project
        self.projects = [p for p in self.projects if p.id != project_id]
        # Remove all tasks belonging to this project
        self.tasks = [t for t in self.tasks if t.project_id != project_id]

    def delete_task(self, task_id: int) -> None:
        """
        Delete a specific task

        Args:
            task_id (int): ID of the task to delete
        """
        self.tasks = [t for t in self.tasks if t.id != task_id]
