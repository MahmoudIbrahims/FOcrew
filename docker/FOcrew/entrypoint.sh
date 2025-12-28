#!/bin/bash
set -e

echo "Running database migrations..."

cd /app/Models/db_schemes/
alembic upgrade head

cd /app

echo "Starting FastAPI..."

exec "$@"