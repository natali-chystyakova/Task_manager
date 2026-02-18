**Task Manager**
---
##  Description 
Task Manager is a simple and intuitive web application for managing projects and tasks.
It is designed for people who want to increase productivity, stay organized, and clearly control their workflow.

The application allows users to create projects, manage tasks inside them, set priorities, assign deadlines, and track completion status — all in a clean and responsive interface.
---

## :arrow_forward: Functional Requirements 
* Projects

- Create projects

- Update projects

- Delete projects

* Tasks

- Add tasks to projects

- Update tasks

- Delete tasks

- Set task priority

- Set task deadline

- Mark tasks as Done
---

##  :wrench: Technical Requirements

+ Backend: Python 3.13 + Django 5.2
+ Frontend:
- HTML
- CSS (Bootstrap 5)
- HTMX
+ Database: PostgreSQL
+ Containerization: Docker + Docker Compose
+ Responsive UI: Bootstrap Grid (desktop + mobile)

---
##  :wrench: Dependencies:
* webargs==8.2.0 
* pre-commit==3.2.2 
* pyupgrade==3.3.1 
* black==23.3.0 
* flake8==6.0.0 
* autoflake==2.0.2 
* requests==2.28.2 
* Django==5.2 
* Pillow>=11.0.0 
* crispy-bootstrap5==0.7 
* django-environ==0.10.0 
* psycopg[binary]>=3.1 
* django-allauth==65.14.1 
* django-htmx==1.27.0

---
##  :rocket: Project Setup
1. Initialize development environment
* make init-dev: Installs dependencies and sets up pre-commit hooks.
2. Initialize config files
* make init-config-i-project: Creates .env and docker override config.
3. Run project in Docker (local development)
* make d-run-i-local-dev
4. Apply migrations
* make migrations 
* make migrate
5. Run project locally (without Docker)
* make project-i-run
6. Pre-commit hooks
* make pre-commit-run-all

---

##  :broom: Code Quality Tools
The project uses automated code quality tools:
* Black — formatter
* Flake8 — linting
* Autoflake — remove unused imports
* Pre-commit hooks — run checks before commits
---

