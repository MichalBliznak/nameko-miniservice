#!/usr/bin/env bash

until curl -i -u ${RABBIT_USER}:${RABBIT_PASSWORD} http://${RABBIT_HOST}:${RABBIT_MGMT_PORT}/api/overview -m 5 2>&1 | grep management_version > /dev/null; do
    echo "$(date) - Waiting for RabbitMQ cluster..."
    sleep 3
done

until nc -z ${REDIS_HOST} ${REDIS_PORT}; do
    echo "$(date) - Waiting for Redis..."
    sleep 3
done

# flask run -h ${GATEWAY_HOST} -p ${GATEWAY_PORT}
gunicorn --workers 4 --worker-class sync --bind ${GATEWAY_HOST}:${GATEWAY_PORT} app:app