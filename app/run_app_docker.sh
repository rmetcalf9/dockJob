#!/bin/bash

if [[ E${FRONTEND_APP_DIR} == "E" ]]; then
  echo "Error - FRONTEND_APP_DIR not specified"
  exit 1
fi
if [[ E${APP_DIR} == "E" ]]; then
  echo "Error - APP_DIR not specified"
  exit 1
fi

VERSION=
if [ -f ${APP_DIR}/../VERSION ]; then
  VERSION=$(cat ${APP_DIR}/../VERSION)
fi
if [ -f ${APP_DIR}/../../VERSION ]; then
  VERSION=$(cat ${APP_DIR}/../../VERSION)
fi
if [ E${VERSION} = 'E' ]; then
  echo 'Can not find version file in standard locations'
  exit 1
fi
if [ E${API_URL} = 'E' ]; then
  echo 'Error - API_URL enviroment variable not set'
  exit 1
fi

_term() { 
  echo "Caught SIGTERM signal!" 
  kill -TERM "$child" 2>/dev/null
}

trap _term SIGTERM

python3 -u ${APP_DIR}/app.py DOCKER ${VERSION} ${FRONTEND_APP_DIR} ${API_URL} '[]' &

child=$! 
wait "$child"


exit 0
