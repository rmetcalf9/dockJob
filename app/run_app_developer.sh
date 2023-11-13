#!/bin/bash

PYTHON_CMD=python3
if [ E${EXTPYTHONCMD} != "E" ]; then
  PYTHON_CMD=${EXTPYTHONCMD}
fi

APP_DIR=.

export APIAPP_MODE=DEVELOPER
export APIAPP_FRONTEND=_
export APIAPP_APIURL=http://localhost:8098/api
export APIAPP_APIDOCSURL=http://localhost:8098/apidocs
export APIAPP_FRONTENDURL=http://localhost:8098/frontend
export APIAPP_APIACCESSSECURITY=[]
export APIAPP_USERFORJOBS=dockjobuser
export APIAPP_GROUPFORJOBS=dockjobgroup
export APIAPP_OBJECTSTORECONFIG="{\"Type\":\"SimpleFileStore\", \"BaseLocation\": \"./test/TestFileStore\"}"
export APIAPP_COMMON_ACCESSCONTROLALLOWORIGIN="http://localhost:8080,http://localhost:8081,http://superego:9000,http://localhost:9000"
export APIAPP_MONITORCHECKTEMPSTATECONFIG"{\"username\":\"user\", \"password\": \"pass\"}"
export APIAPP_PORT=8098

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
echo "PYTHON_CMD: $PYTHON_CMD"
${PYTHON_CMD} ./src/app.py
RES=$?

if [ $RES -ne 0 ]; then
  echo "Process Errored"
  read -p "Press enter to continue"
fi
