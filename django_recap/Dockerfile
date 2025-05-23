FROM python:3.12-slim

WORKDIR /workspace

COPY . .

RUN python3 manage.py collectstatic --noinput

CMD ["gunicorn","django_recap.wsgi:application","--bind","0.0.0.0:8000"]
