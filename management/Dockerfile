FROM python:3-alpine

ENV FLASK_APP=switch2
ENV GUNICORN_CMD_ARGS="--workers=2 --bind=0.0.0.0:5000 --access-logfile=- --error-logfile=-"

EXPOSE 5000

LABEL traefik.frontend.rule="Host:switch2.tangogolf.lan"

RUN pip install --no-cache-dir \
  flask \
  flask_redis \
  pika \
  requests \
  gunicorn

COPY setup.py /switch2/
COPY switch2 /switch2/switch2

RUN pip install --no-cache-dir -e /switch2

CMD ["gunicorn", "switch2:app"]
