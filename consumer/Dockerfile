FROM python:3-alpine3.13

RUN mkdir /var/run/supervisord /var/log/supervisord

RUN apk add --update --no-cache \
  gcc \
  musl-dev \
  libffi-dev \
  openssl-dev \
  supervisor

RUN pip install --no-cache-dir \
  pika \
  requests

COPY etc/supervisord.conf /etc/supervisord.conf

COPY consumer/ /consumer/

CMD ["supervisord", "-c", "/etc/supervisord.conf"]

