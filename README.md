# Student records (Django)
A staff-only CRUD learning project with validated forms, CSRF-protected POST deletion and permission checks.

## Local setup (Python 3.12)
```sh
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(48))')"
export DEBUG=True
cd student_project
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
On PowerShell, use `$env:SECRET_KEY = python -c "import secrets; print(secrets.token_urlsafe(48))"` and `$env:DEBUG = "True"`.
Visit http://127.0.0.1:8000/students/ and log in with a staff/superuser account. Ordinary accounts cannot access student records.

## Tests
With the same environment, run `python manage.py test students`.

## Deployment
Set a persistent random SECRET_KEY, DEBUG=False and ALLOWED_HOSTS to the actual hostname. Use HTTPS and persistent database storage. Rotate the previously committed key wherever it was used; removing it from this branch does not remove Git history. Do not use real student data in a public demo.
