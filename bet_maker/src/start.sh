#!/bin/bash
sleep 5
cd /app
alembic upgrade head
gunicorn app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
