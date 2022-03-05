FROM rabbitmq:3.8.27-management-alpine

RUN rabbitmq-plugins enable --offline rabbitmq_prometheus

COPY /etc/rabbitmq/rabbitmq.conf /etc/rabbitmq/rabbitmq.conf
