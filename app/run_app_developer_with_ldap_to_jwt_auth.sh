#!/bin/bash

APP_DIR=.

export APIAPP_MODE=DEVELOPER
export APIAPP_FRONTEND=_
export APIAPP_APIURL=http://somefunnyhostname.com:5080/api
export APIAPP_APIDOCSURL=http://somefunnyhostname.com:5080/apidocs
export APIAPP_FRONTENDURL=http://somefunnyhostname.com:5080/frontend
export APIAPP_APIACCESSSECURITY="[{\"type\": \"basic-auth-login-toget-jwttoken\", \"loginurl\": \"http://somefunnyhostname.com:5079/login/\", \"cookiename\": \"jwt-auth-cookie\" }]"
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


python3 ./src/app.py
exit 0
