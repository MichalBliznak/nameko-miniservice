#!/usr/bin/env bash

until curl -i -u ${RABBIT_USER}:${RABBIT_PASSWORD} http://${RABBIT_HOST}:${RABBIT_MGMT_PORT}/api/overview -m 5 2>&1 | grep management_version > /dev/null; do
    echo "$(date) - Waiting for RabbitMQ cluster..."
    sleep 3
done

nameko run --config config.yml heartbeat