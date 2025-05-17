FROM postgres:17

RUN apt-get update \
    && apt-get install postgis -y

ADD ./compose/postgres/start.sh /docker-entrypoint-initdb.d
