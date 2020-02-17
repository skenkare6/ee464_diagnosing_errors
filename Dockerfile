FROM mysql:latest

ENV MYSQL_ROOT_PASSWORD=s3cr3t
ENV MYSQL_DATABASE: test

ADD schema.sql /docker-entrypoint-initdb.d
