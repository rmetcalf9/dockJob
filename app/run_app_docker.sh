#!/bin/bash

if [[ E${FRONTEND_APP_DIR} == "E" ]]; then
  echo "Error - FRONTEND_APP_DIR not specified"
  exit 1
fi
if [[ E${APP_DIR} == "E" ]]; then
  echo "Error - APP_DIR not specified"
  exit 1
fi


_term() { 
  echo "Caught SIGTERM signal!" 
  kill -TERM "$child" 2>/dev/null
}

trap _term SIGTERM

python3 -u ${APP_DIR}/app.py DOCKER $(cat ${APP_DIR}/../VERSION) ${FRONTEND_APP_DIR} &

child=$! 
wait "$child"


exit 0
