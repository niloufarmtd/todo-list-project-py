from fastapi import FastAPI
from app.api.routes import projects, tasks 

app = FastAPI(
    title="TodoList API",
    description="A simple TodoList API with FastAPI", 
    version="1.0.0"
)

app.include_router(projects.router, prefix="/api/v1", tags=["projects"])
app.include_router(tasks.router, prefix="/api/v1", tags=["tasks"])  

@app.get("/")
def hello():
    return {"message": "Hello! My API is working!"}

@app.get("/test") 
def test():
    return {"status": "ok", "version": "1.0.0"}