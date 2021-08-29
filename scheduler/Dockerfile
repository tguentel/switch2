FROM python:3-alpine3.13

RUN apk add --update --no-cache \
  py3-pip \
  python3

RUN pip install --no-cache-dir \
  requests

COPY bin /scheduler/bin
COPY scripts/update-device-status.py /scheduler/update-device-status.py

CMD ["python", "/scheduler/update-device-status.py"]
