FROM python:3.10.2-slim

ADD . /app/src
WORKDIR /app/src
EXPOSE 8888

ENTRYPOINT [ "python3", "main.py" ]