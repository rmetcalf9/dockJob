#!/bin/bash

#Hardcoded here
export APIAPP_MODE=DOCKER

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

_term() { 
  echo "run_app_docker.sh - Caught SIGTERM signal!" 
  kill -TERM "$child" 2>/dev/null
}

trap _term SIGTERM

if [ E${DOCKERRUN_USERHOSTFILE} != 'E' ]; then
  echo 'DOCKERRUN_USERHOSTFILE set evaluating APIAPP_ enviroment variables with DOCKERRUN_USERHOST set'
  if [ ! -f ${DOCKERRUN_USERHOSTFILE} ]; then
    echo 'ERROR ${DOCKERRUN_USERHOSTFILE} not present'
    exit 1
  fi
  DOCKERRUN_USERHOST=$(cat ${DOCKERRUN_USERHOSTFILE})
  VARSTOUPDATE=$(env | grep "^APIAPP_")
  C=0
  for i in ${VARSTOUPDATE}; do
    ((C++))
    eval "${i}"
  done
  echo "  ${C} variables evaluated"
fi

python3 -u "${APP_DIR}/app.py" &

child=$! 
wait "$child"


exit 0
