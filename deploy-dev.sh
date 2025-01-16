#!/usr/bin/env bash

docker build -t fastapi_docker -f local.Dockerfile .
docker save -o fastapi_docker.tar fastapi_docker
zip fastapi_docker.zip fastapi_docker.tar
