#!/usr/bin/env bash

until nc -z ${RABBIT_HOST} ${RABBIT_PORT}; do
    echo "$(date) - waiting for rabbitmq..."
    sleep 3
done

export FLASK_APP=app.py
export FLASK_ENV=development
flask run -p 8000