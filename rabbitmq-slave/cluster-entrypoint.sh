#!/bin/bash

set -e

# Wait a while for the master node to start
echo "Sleeping for 10s (waiting for master node to run)..."
sleep 10s

# Start RMQ from entry point.
# This will ensure that environment variables passed
# will be honored
/usr/local/bin/docker-entrypoint.sh rabbitmq-server -detached

# Do the cluster dance
rabbitmqctl stop_app
rabbitmqctl join_cluster rabbit@rabbit-master

# Stop the entire RMQ server. This is done so that we
# can attach to it again, but without the -detached flag
# making it run in the foreground
rabbitmqctl stop

# Wait a while for the app to really stop
echo "Sleeping for 2s (Stopping node)..."
sleep 2s

# Start it
rabbitmq-server