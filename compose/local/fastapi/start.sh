#! /usr/bin/env bash


# Run migrations
alembic upgrade head;

uvicorn app.main:app --host 0.0.0.0 --port 80
