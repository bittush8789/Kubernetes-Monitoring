# Backend Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY main.py .
RUN pip install fastapi uvicorn prometheus_client

EXPOSE 8000

CMD ["python", "main.py"]
