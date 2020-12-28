#!/bin/bash

. ${PWD}/.env

WEB_APP_DIRECTORY_PATH=${PWD}/web
COMMON_MODELS_PY_PATH=${PWD}/common/models.py

docker run \
    --rm \
    --network ${DOCKER_NAME}_net \
    --name migrate \
    -w /source \
    --env-file ${PWD}/.env \
    -v ${WEB_APP_DIRECTORY_PATH}:/source \
    -v ${COMMON_MODELS_PY_PATH}:/source/models.py \
    coin_alarm_web:base /bin/bash -c /source/migrate.sh