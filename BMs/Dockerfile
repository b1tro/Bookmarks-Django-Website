FROM python:3.9.20-slim

ENV PYTHONDONTWRITECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

CMD python manage.py makemigrations \
    && python manage.py migrate \
    && python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@admin.com', 'admin'); from account.models import Profile; Profile.objects.filter(user=User.objects.get(username='admin')).exists() or Profile(user=User.objects.get(username='admin')).save()"  \
    && python manage.py collectstatic --noinput \
    && gunicorn --bind 0.0.0.0:8000 BMs.wsgi:application

