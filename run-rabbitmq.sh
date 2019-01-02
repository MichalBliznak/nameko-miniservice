#!/usr/bin/env bash

docker run -d --hostname rabbitmq-localhost --name rabbitmq -p 15672:15672 -p 5672:5672 rabbitmq:3-management
