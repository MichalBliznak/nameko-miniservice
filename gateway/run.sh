#!/usr/bin/env bash

until nc -z ${RABBIT_HOST} ${RABBIT_PORT}; do
    echo "$(date) - waiting for rabbitmq..."
    sleep 3
done

# flask run -h ${GATEWAY_HOST} -p ${GATEWAY_PORT}
gunicorn --workers 4 --worker-class sync --bind ${GATEWAY_HOST}:${GATEWAY_PORT} app:app