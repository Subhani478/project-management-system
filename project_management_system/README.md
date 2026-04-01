# Project Management System

A modern **Django-based Project Management System** with JWT authentication, role-based access, tasks, projects, and team collaboration features.

## ✨ Features

- JWT Authentication (Login + Token Refresh)
- Custom User Model with Roles (Admin, ProjectManager, TeamMember, Viewer)
- Project Management (with status, priority, manager & members)
- Task Management with assignee and progress
- Comment System on tasks
- Role-based Permissions
- Clean RESTful APIs using Django REST Framework

## 🛠️ Tech Stack

- **Backend**: Django 5 + Django REST Framework
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: SQLite (ready for PostgreSQL)

## 🚀 How to Run

```bash
# 1. Clone the repository
git clone https://github.com/Subhani478/project-management-system.git

# 2. Go to project folder
cd project-management-system

# 3. Activate virtual environment
.\venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run migrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Run server
python manage.py runserver
