#!/bin/bash

echo "Waiting for MySQL to start..."

until mysql -h "$MYSQL_HOST" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD"
do
    sleep 1
done

echo "MySQL is up and running!"

cd /usr/src/app/db && alembic upgrade head
cd /usr/src/app/app && uvicorn main:app --reload --port=8000 --host=0.0.0.0
