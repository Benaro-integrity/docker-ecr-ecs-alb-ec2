FROM python:3.11-slim

WORKDIR /app

# Prevent Python from writing .pyc files and buffer outputs (better for container logs)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir flask

COPY . /app

# ALB will target port 80 by default
EXPOSE 80

CMD ["python", "app.py"]
