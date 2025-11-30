from pydantic import BaseModel
from datetime import datetime

class ProjectCreate(BaseModel):
    name: str
    description: str

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime
    
class ProjectUpdate(BaseModel):
    name: str
    description: str
    
    class Config:
        from_attributes = True
        