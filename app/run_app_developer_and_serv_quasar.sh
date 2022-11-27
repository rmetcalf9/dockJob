#!/bin/bash

if [ E${APP_DIR} = 'E' ]; then
  APP_DIR=.
fi

PYTHON_CMD=python3
if [ E${EXTPYTHONCMD} != "E" ]; then
  PYTHON_CMD=${EXTPYTHONCMD}
fi

START_DIR=$(pwd)
cd ../webfrontend/dist/spa-mat
WEBFRONTEND_DIR=$(pwd)
cd ${START_DIR}

export APIAPP_MODE=DEVELOPER
export APIAPP_FRONTEND=${WEBFRONTEND_DIR}
export APIAPP_APIURL=http://cat-sdts.metcarob-home.com/api
export APIAPP_APIDOCSURL=http://cat-sdts.metcarob-home.com/apidocs
export APIAPP_FRONTENDURL=http://cat-sdts.metcarob-home.com/frontend
export APIAPP_APIACCESSSECURITY=[]
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
APIAPP_VERSION=DEVELOPMENT-SERV-${APIAPP_VERSION}

${PYTHON_CMD} ./src/app.py
RES=$?

if [ $RES -ne 0 ]; then
  echo "Process Errored"
  read -p "Press enter to continue"
fi
