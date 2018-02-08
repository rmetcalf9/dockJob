#!/bin/bash

START_DIR=$(pwd)
cd ../webfrontend/dist
WEBFRONTEND_DIR=$(pwd)
cd ${START_DIR}
python3 ./src/app.py DEVELOPER DEVELOPMENT-SERV-$(cat ${APP_DIR}/../VERSION) ${WEBFRONTEND_DIR}
