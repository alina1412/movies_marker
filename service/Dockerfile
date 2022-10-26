FROM python:3.10.5-slim-buster

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# for psycopg2
RUN apt update && \
    apt install --no-install-recommends --no-install-suggests --assume-yes \
    gcc \
    libpq-dev \
    python-dev

RUN python -m pip install --upgrade pip

RUN mkdir -p /app/service
WORKDIR /app

ADD . /app/service

RUN pip install -r /app/service/requirements.txt

CMD ["python", "-m", "service"]
