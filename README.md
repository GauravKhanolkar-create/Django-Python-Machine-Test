# How to Run:

# Setup Environment
mkdir django_machine_test

cd django_machine_test

# Create virtual environment
python -m venv venv

venv\Scripts\activate

# Reuirements
Python 3.8+ installed

MySQL Server installed and running

pip install Django

pip install djangorestframework

pip install mysqlclient

# Create Project Structure
django-admin startproject machine_test .

python manage.py startapp api

# Update settings.py with your local MySQL credentials

# Run Migrations
python manage.py makemigrations

python manage.py migrate

# Create Superuser
python manage.py createsuperuser

Username: admin

Email: admin@example.com

Password: admin123

# Start the Server
python manage.py runserver

# Using the Application
Open browser and go to: http://127.0.0.1:8000/admin/

Login with superuser credentials
