#!/bin/bash

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
  echo "Caught SIGTERM signal!" 
  kill -TERM "$child" 2>/dev/null
}

trap _term SIGTERM

python3 -u "${APP_DIR}/app.py" "DOCKER" "${APIAPP_VERSION}" "${FRONTEND_APP_DIR}" "${API_URL}" "${AUTH_OPTIONS}" &

child=$! 
wait "$child"


exit 0
