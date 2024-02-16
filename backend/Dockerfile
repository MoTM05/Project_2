FROM python:3.12-slim-bullseye
ENV LANG=C.UTF-8

RUN apt-get update && apt-get install -y libpq-dev gcc

RUN mkdir -p /app
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
RUN mkdir -p static media logs
EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]
