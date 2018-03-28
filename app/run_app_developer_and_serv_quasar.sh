#!/bin/bash

if [ E${APP_DIR} = 'E' ]; then
  APP_DIR=.
fi

START_DIR=$(pwd)
cd ../webfrontend/dist
WEBFRONTEND_DIR=$(pwd)
cd ${START_DIR}

export APIAPP_MODE=DEVELOPER
export APIAPP_FRONTEND=${WEBFRONTEND_DIR}
export APIAPP_APIURL=http://localhost:80/api
export APIAPP_APIACCESSSECURITY=[]


export APIAPP_VERSION=
if [ -f ${APP_DIR}/../VERSION ]; then
  APIAPP_VERSION=${0}-$(cat ${APP_DIR}/../VERSION)
fi
if [ -f ${APP_DIR}/../../VERSION ]; then
  APIAPP_VERSION=${0}-$(cat ${APP_DIR}/../../VERSION)
fi
if [ E${APIAPP_VERSION} = 'E' ]; then
  echo 'Can not find version file in standard locations'
  exit 1
fi
APIAPP_VERSION=DEVELOPMENT-SERV-${APIAPP_VERSION}

python3 ./src/app.py
