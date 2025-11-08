#!/bin/bash
set -e

echo "Run migrations"
alembic upgrade head

python -m models.create_schema

exec uvicorn main:app --reload
