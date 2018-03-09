#!/bin/bash

APP_DIR=.

export APIAPP_MODE=DEVELOPER
export APIAPP_FRONTEND=_
export APIAPP_APIURL=http://somefunnyhostname.com:5080/api
export APIAPP_APIDOCSURL=http://somefunnyhostname.com:5080/apidocs/
export APIAPP_APIACCESSSECURITY=[]
export APIAPP_USERFORJOBS=dockjobuser
export APIAPP_GROUPFORJOBS=dockjobgroup


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


#Python app reads parameters from environment variables
python3 ./src/app.py
