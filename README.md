# Django Nully Backend API Template

Easy to set up Django backend API template with PostgreSQL database.

## Features

- Social Login (Google, Naver, Kakao)

## Requirements

- Python 3.11
- PostgreSQL 13.12
- Redis (Celery, Cache)

## CI/CD

- GitHub Actions

## Getting Started

```shell
# Clone the repository

# Create a virtual environment in the root directory
python -m venv venv

# Activate the virtual environment
# Windows
source venv/Scripts/activate
# Linux
source venv/bin/activate

# Install the requirements
pip install -r requirements.txt

# Define .env file
fab2 generate-env

# Define settings file
# local, development, production
export DJANGO_SETTINGS_MODULE=XXXX.settings.local

# Migrate the database
python manage.py migrate

# Run the server
python manage.py runserver
```
