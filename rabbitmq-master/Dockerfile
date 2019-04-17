FROM rabbitmq:3-management

COPY cluster-entrypoint.sh /usr/local/bin/cluster-entrypoint.sh
COPY rabbitmq.conf /etc/rabbitmq
COPY definitions.json /etc/rabbitmq

RUN chmod +x /usr/local/bin/cluster-entrypoint.sh
RUN chmod +rw /etc/rabbitmq/rabbitmq.conf
RUN chmod +rw /etc/rabbitmq/definitions.json

ENTRYPOINT /usr/local/bin/cluster-entrypoint.sh
