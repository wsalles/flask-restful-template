FROM python:3.9-alpine

WORKDIR /app
COPY . .

RUN apk add --no-cache \
        gcc linux-headers libc-dev \
        mariadb-dev python3-dev libffi-dev openssl-dev \
        jpeg-dev zlib-dev bash

ENV TZ="America/Sao_Paulo"
RUN apk add tzdata

RUN rm -rf \
        /usr/local/share/doc \
        /usr/local/share/man \
        /var/cache/apk/* \
    && find /usr/local -name '*.a' -delete


RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["uwsgi", "--ini", "/app/uwsgi.ini"]