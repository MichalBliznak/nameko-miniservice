TODOs
=====

* Optionally move JWT secret to Vault server (https://dynaconf.readthedocs.io/en/latest/guides/sensitive_secrets.html)
* Deploy in microk8s
* Move credentials to Postgres
* Use RabbitMQ HA cluster with Nameko microservices (https://medium.com/@oprearocks/set-up-a-rabbitmq-cluster-on-your-laptop-using-docker-4276555b0f28, https://groups.google.com/forum/#!topic/nameko-dev/Ohl_tf0YY1o)
* Add HA Proxy in front of RabbitMQ cluster to load balance access to its Management UI (https://github.com/pardahlman/docker-rabbitmq-cluster)
