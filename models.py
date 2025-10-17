from datetime import datetime

class Project:
    """Model for representing a project"""
    
     def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description
        self.created_at = datetime.now()
    
    def __str__(self):
        return f"Project {self.id}: {self.name}"


class Task:
    """Model for representing a task"""
    
     def __init__(self, id, title, description, project_id, deadline=None):
            self.id = id
            self.title = title
            self.description = description
            self.status = "todo"  # default status
            self.project_id = project_id
            self.deadline = deadline  
            self.created_at = datetime.now()

      def __str__(self):
         deadline_str = self.deadline.strftime("%Y-%m-%d") if self.deadline else "No deadline"
         return f"Task {self.id}: {self.title} ({self.status}) - Deadline: {deadline_str}"
