#!/usr/bin/env bash

docker-compose up -d sentry

sleep 5

# If this is a new database, you'll need to run upgrade
docker-compose exec sentry sentry upgrade

docker-compose down
