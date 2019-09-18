#!/bin/bash

microk8s.kubectl exec $(microk8s.kubectl get pod -l io.kompose.service=sentry -o name) -i -t -- sentry upgrade

microk8s.kubectl exec $(microk8s.kubectl get pod -l io.kompose.service=sentry -o name) -i -t -- sentry createuser
