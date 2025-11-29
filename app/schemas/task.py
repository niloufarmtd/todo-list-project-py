from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TaskBase(BaseModel):
    title: str
    description: str
    deadline: Optional[datetime] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    status: Optional[str] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str     
    deadline: Optional[datetime]
    status: str
    project_id: int
    created_at: datetime
    closed_at: Optional[datetime]

    class Config:
        orm_mode = True
