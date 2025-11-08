#!/bin/bash
set -e

echo "Run migrations"
alembic upgrade head

exec uvicorn main:app --reload
