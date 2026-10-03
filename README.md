# Student Management (Django, black & white)

    python -m venv venv
    source venv/bin/activate        # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py createsuperuser   # for the admin panel
    python manage.py runserver

App: http://127.0.0.1:8000/    Admin: http://127.0.0.1:8000/admin/
Add a course first, then students.
