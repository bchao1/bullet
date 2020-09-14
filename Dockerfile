FROM python:3-slim

WORKDIR /usr/src/app

RUN pip install --no-cache-dir bullet==2.0.0

CMD [ "bash" ]
