#!/bin/bash

APP_DIR=.

export APIAPP_MODE=DEVELOPER
export APIAPP_FRONTEND=_
export APIAPP_APIURL=localhost
export APIAPP_APIACCESSSECURITY=[]


export APIAPP_VERSION=
if [ -f ${APP_DIR}/../VERSION ]; then
  APIAPP_VERSION=$(cat ${APP_DIR}/../VERSION)
fi
if [ -f ${APP_DIR}/../../VERSION ]; then
  APIAPP_VERSION=$(cat ${APP_DIR}/../../VERSION)
fi


#Python app reads parameters from environment variables
python3 ./src/app.py
