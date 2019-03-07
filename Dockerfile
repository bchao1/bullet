FROM python:3-slim

# install latest bullet from source code
WORKDIR /usr/src/temp

COPY . .

RUN pip install --no-cache . \
    && rm -rf /usr/src/temp

# change workspace
WORKDIR /usr/src/app

CMD [ "bash" ]
