FROM postgres:17

RUN apt-get update \
    && apt-get -y install postgis

ADD ./compose/test/postgres/start.sh /docker-entrypoint-initdb.d
ADD ./.fixtures/00_schema.sql /docker-entrypoint-initdb.d
ADD ./.fixtures/02_triggers.sql /docker-entrypoint-initdb.d
