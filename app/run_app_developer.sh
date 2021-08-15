#!/bin/bash

APP_DIR=.

export APIAPP_MODE=DEVELOPER
export APIAPP_FRONTEND=_
export APIAPP_APIURL=http://localhost/api
export APIAPP_APIDOCSURL=http://localhost/apidocs
export APIAPP_FRONTENDURL=http://localhost/frontend
export APIAPP_APIACCESSSECURITY=[]
export APIAPP_USERFORJOBS=dockjobuser
export APIAPP_GROUPFORJOBS=dockjobgroup
export APIAPP_OBJECTSTORECONFIG="{\"Type\":\"SimpleFileStore\", \"BaseLocation\": \"./test/TestFileStore\"}"
export APIAPP_COMMON_ACCESSCONTROLALLOWORIGIN="http://localhost:8080,http://localhost:8081"
export APIAPP_MONITORCHECKTEMPSTATECONFIG"{\"username\":\"user\", \"password\": \"pass\"}"

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


#Python app reads parameters from environment variables
python3.6 ./src/app.py

