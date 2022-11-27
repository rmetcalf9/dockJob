#!/bin/bash

APP_DIR=.

PYTHON_CMD=python3
if [ E${EXTPYTHONCMD} != "E" ]; then
  PYTHON_CMD=${EXTPYTHONCMD}
fi

export APIAPP_MODE=DEVELOPER
export APIAPP_FRONTEND=_
export APIAPP_APIURL="http://localhost:80/api"
export APIAPP_FRONTENDURL="http://localhost.com:80/frontend"
export APIAPP_APIACCESSSECURITY="[{\"type\": \"basic-auth\" }]"
export APIAPP_USERFORJOBS=dockjobuser
export APIAPP_GROUPFORJOBS=dockjobgroup


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
APIAPP_VERSION=DEVELOPMENT-${APIAPP_VERSION}


${PYTHON_CMD} ./src/app.py
RES=$?

if [ $RES -ne 0 ]; then
  echo "Process Errored"
  read -p "Press enter to continue"
fi

