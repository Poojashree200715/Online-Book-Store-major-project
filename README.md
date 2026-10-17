# BookHaven – Django Online Book Store

## Setup
```
python -m venv venv
venv\Scripts\activate        # Windows  (Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
python manage.py makemigrations store
python manage.py migrate
python manage.py seed_books
python manage.py createsuperuser
python manage.py runserver
```
Site: http://127.0.0.1:8000/  Admin: http://127.0.0.1:8000/admin/

## Gemini key (Team 4)
Set it as an environment variable, never commit it:
```
set GEMINI_API_KEY=your_key_here        # Windows
export GEMINI_API_KEY=your_key_here     # Mac/Linux
```
