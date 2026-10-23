# Team 5 – Newsletter, Admin & Tests (drop-in package)

All new code lives in NEW files, so nothing in your teammates' files is overwritten.

## 1. Copy files into the project
- store/models_newsletter.py
- store/views_newsletter.py
- store/admin_newsletter.py
- store/test_newsletter.py
- templates/partials/newsletter_form.html

## 2. Make 5 one-line edits to existing files

store/models.py   (bottom)
    from .models_newsletter import Subscriber  # noqa: F401

store/admin.py    (bottom)
    from . import admin_newsletter  # noqa: F401

store/urls.py
    from .views_newsletter import subscribe
    # inside urlpatterns:
    path('subscribe/', subscribe, name='subscribe'),

templates/base.html  (inside the footer)
    {% include 'partials/newsletter_form.html' %}

bookstore/settings.py  (bottom)
    from django.contrib.messages import constants as msg
    MESSAGE_TAGS = {msg.ERROR: 'danger'}

If store/urls.py uses app_name = 'store', change the form action to
{% url 'store:subscribe' %}.
If Team 2 already made a Subscriber model, use theirs instead and skip
models_newsletter.py (and update the imports in the other files).

## 3. Run
    python manage.py makemigrations store
    python manage.py migrate
    python manage.py test store
    python manage.py runserver

## 4. Git
    git checkout -b team5-admin-newsletter
    git add .
    git commit -m "Add newsletter subscription, admin config and tests"
    git push origin team5-admin-newsletter
