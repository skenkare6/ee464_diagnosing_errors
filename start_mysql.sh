#!/bin/sh



docker build -t dev-mysql . && \
docker run -d dev-mysql
