class InMemoryStorage:
    """In-memory storage for projects and tasks"""
    
    def __init__(self):
        self.projects = []
        self.tasks = []
        self.next_project_id = 1
        self.next_task_id = 1
    
    def add_project(self, project):
        """Add a new project and assign auto-increment ID"""
        project.id = self.next_project_id
        self.next_project_id += 1
        self.projects.append(project)
        return project
    
    def add_task(self, task):
        """Add a new task and assign auto-increment ID"""
        task.id = self.next_task_id
        self.next_task_id += 1
        self.tasks.append(task)
        return task
    
    def get_all_projects(self):
        """Get all projects"""
        return self.projects
    
    def get_tasks_by_project(self, project_id):
        """Get all tasks for a specific project"""
        return [task for task in self.tasks if task.project_id == project_id]
    
    def delete_project(self, project_id):
        """Delete a project and all its tasks (Cascade Delete)"""
        # Remove project
        self.projects = [p for p in self.projects if p.id != project_id]
        # Remove all tasks belonging to this project
        self.tasks = [t for t in self.tasks if t.project_id != project_id]
    
    def delete_task(self, task_id):
        """Delete a specific task"""
        self.tasks = [t for t in self.tasks if t.id != task_id]
