# todo-list-project
**ToDoList - Python OOP**   A clean ToDoList application built with Python OOP principles. Features project/task management with in-memory storage, following PEP8 standards and using Poetry for dependencies. Perfect for learning modular Python development.

# 🚀 ToDo List - Python OOP (In-Memory)

A project and task management system implemented with Object-Oriented Programming in Python.

## 📋 Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Coding Conventions](#coding-conventions)
- [Version Control](#version-control)
- [Development](#development)
- [Future Phases](#future-phases)

## 🎯 Introduction

This project is a ToDo List management system developed using **Incremental Development** and **Agile** methodologies. In Phase 1, data is stored In-Memory.

### Implemented User Stories:

1. **Create Project** - Create new projects with quantity limits
2. **Edit Project** - Update project name and description
3. **Delete Project** - Delete project with all its tasks (Cascade Delete)
4. **Add Task** - Create new tasks within projects
5. **Update Task Status** - Change task status (todo/doing/done)
6. **Edit Task** - Modify task details
7. **Delete Task** - Remove individual tasks
8. **List Projects** - View all projects
9. **List Project Tasks** - View tasks for a specific project

## ✨ Features

### Functional Requirements
- ✅ Complete project management (create, edit, delete, list)
- ✅ Complete task management (create, edit, delete, update status)
- ✅ Name and description length validation
- ✅ Project/task quantity limits via `.env` file
- ✅ Valid task statuses: `todo`, `doing`, `done`
- ✅ Deadline date validation

### Non-Functional Requirements
- 🏗️ Modular OOP design
- 📝 Full PEP8 compliance and Python conventions
- 🔧 Maintainable and easily extensible code
- 🎯 User-friendly error messages
- 🚀 Ready for future phases (Persistency, Web API)

## Project Structure

### src/
├── core/           # Business logic
│   ├── project.py
│   ├── task.py
│   └── exceptions.py
├── storage/        # Data layer
│   └── in_memory_storage.py
└── ui/            # Interface
    └── cli.py


## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Poetry (for dependency management)


### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/niloufarmtd/todo-list-project-py.git
   cd todo-list-python
   
2. **Install Poetry (if not installed):**

bash
pip install poetry

3. **Install dependencies:**

bash
poetry install

4. **Activate virtual environment:**

bash
poetry shell

5. **Setup environment file:**

bash
cp .env.example .env
# Edit .env file with your values


## Environment Settings

### Create a .env file with the following settings:

text
MAX_NUMBER_OF_PROJECTS=50
MAX_NUMBER_OF_TASKS_PER_PROJECT=200


## 🎮 Usage

### Running the Application
bash
poetry run python -m src.ui.cli
Example Commands


## Create new project:

### > create_project
Project name: Learning Project
Description: A sample project for educational purposes


## Add task:

### > add_task
Project ID: 1
Task title: Study documentation
Description: Complete study of phase 1 documentation
Deadline (YYYY-MM-DD): 2024-10-20


## Update task status:

### > update_task_status
Project ID: 1
Task ID: 1
New status (todo/doing/done): doing


## List all projects:

### > list_projects


## List project tasks:

### text
> list_project_tasks
Project ID: 1


## 📏 Coding Conventions

### This project fully complies with the following standards:

PEP8 - Python style guide

PEP484 - Type hints

Google Style Docstrings - Documentation

Meaningful Names - Descriptive naming    


## 🔄 Version Control

### Branching Strategy
main - Stable release versions

develop - Main development branch

feature/* - New features

bugfix/* - Bug fixes


## Commit Guidelines
### Use Conventional Commits format

Make small, focused commits

Write clear and meaningful commit messages


## 🚀 Development

### Adding Dependencies
bash
poetry add package-name

## Running Tests
### bash
poetry run pytest


## Code Formatting
### bash
poetry run black src/
poetry run isort src/

## Code Quality
bash
poetry run flake8 src/
poetry run mypy src/

## 📅 Future Phases
### Development Roadmap
Phase 2: Persistent storage (JSON/SQLite)

Phase 3: Web application with FastAPI

Phase 4: Comprehensive automated testing


##🤝 Contributing
### We welcome contributions! Please follow these steps:

Fork the project

Create your feature branch: git checkout -b feature/AmazingFeature

Commit your changes: git commit -m 'Add some AmazingFeature'

## Sample Feature Branch
This is a sample feature branch created to demonstrate Git workflow.

Push to the branch: git push origin feature/AmazingFeature

Open a Pull Request

## 📄 License
### This project is licensed under the MIT License.


## 🚀 Development Workflow

### Branch Strategy:
- `main` 🛡️ - Protected branch for stable releases only
- `develop` - Main development branch  
- `feature/*` - Feature branches for new functionality

### Git Flow:
1. **Feature Development**:
   ```bash
   git checkout develop
   git checkout -b feature/feature-name
   # Make changes and commit
   git push origin feature/feature-name
   
2. **Code Review & Merge**:

Create Pull Request from feature/* to develop

Review and test changes

Merge after approval

3. **Release to Main**:

Only stable, tested versions go to main

Create Pull Request from develop to main

Merge after final verification
