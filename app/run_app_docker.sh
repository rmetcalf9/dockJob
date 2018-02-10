#!/bin/bash

#Check the input paramaters are correct
# Can be called with 0 params which runs the process
# 1 param which must be HEALTHCHECK which runs a healthcheck
if [[ $# != 0 ]]
then
  if [[ $# != 1 ]]
  then
    echo "ERROR - Must be called with one parameter"
    exit 1
  fi
  echo "Healthcheck not implemented"
  exit 0
fi

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
