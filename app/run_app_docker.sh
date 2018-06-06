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
  kill -TERM "$child_nginx" 2>/dev/null
  kill -TERM "$child_uwsgi" 2>/dev/null
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

uwsgi --ini /uwsgi.ini &
child_uwsgi=$! 
nginx -g 'daemon off;' &
child_nginx=$! 

wait "$child_uwsgi"

##wait "$child_nginx"
##Not waiting for nginx. Otherwise when python app terminates but nginx doesn't
## the container dosen't stop
## instead we kill nginx if the python app has stopped
kill -TERM "$child_nginx" 2>/dev/null
wait "$child_nginx"

exit 0
