# People Desk Employee Management

A Django employee and department manager with server-rendered HTML screens and a Django REST Framework API. The project uses SQLite by default for a quick local start and supports MySQL through environment settings.

## Start locally

Python 3.10 or newer is recommended.

```powershell
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/` and sign in with the superuser credentials. Employee and department records are also available in Django admin at `/admin/`.

## Use MySQL

Create a database using `utf8mb4`, then edit `.env` with the database details you provide:

```dotenv
DB_ENGINE=mysql
DB_NAME=employee_management
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

Run `python manage.py migrate` after configuring the connection. The `.env` file is ignored by Git; do not commit production secrets. Change `DJANGO_SECRET_KEY`, turn `DJANGO_DEBUG` off, and set `DJANGO_ALLOWED_HOSTS` before deployment.

## Features

- Login-protected dashboard, employee directory, search and filters.
- Open account registration; new accounts are signed in and redirected to the dashboard immediately.
- Create, view, update, and delete employees, with confirmation before deletion.
- Department creation, editing, and deletion; departments with assigned employees cannot be deleted.
- Dashboard counts for total and active employees, departments, and recently added records.
- Authenticated REST API for employee and department CRUD at `/api/employees/` and `/api/departments/`.
- Django admin at `/admin/`.

The API accepts Django session authentication and HTTP Basic authentication. Attendance and leave workflows are not included in this initial release.