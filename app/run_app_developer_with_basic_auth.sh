#!/bin/bash

APP_DIR=.

export APIAPP_MODE=DEVELOPER
export APIAPP_FRONTEND=_
export APIAPP_APIURL="http://localhost:80/api"
export APIAPP_APIACCESSSECURITY="[{\"type\": \"basic-auth\" }]"


export APIAPP_VERSION=
if [ -f ${APP_DIR}/../VERSION ]; then
  APIAPP_VERSION=$(cat ${APP_DIR}/../VERSION)
fi
if [ -f ${APP_DIR}/../../VERSION ]; then
  APIAPP_VERSION=$(cat ${APP_DIR}/../../VERSION)
fi
if [ E${APIAPP_VERSION} = 'E' ]; then
  echo 'Can not find version file in standard locations'
  exit 1
fi
APIAPP_VERSION=DEVELOPMENT-${APIAPP_VERSION}


python3 ./src/app.py
exit 0
