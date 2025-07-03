FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["newrelic-admin", "run-program", "gunicorn", "scoreboard.wsgi:application", "--bind", "0.0.0.0:8000"] 