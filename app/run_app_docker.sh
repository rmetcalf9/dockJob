#!/bin/bash

if [[ E${FRONTEND_APP_DIR} == "E" ]]; then
  echo "Error - FRONTEND_APP_DIR not specified"
  exit 1
fi


python3 ./src/app.py DOCKER DEVELOPMENT ${FRONTEND_APP_DIR}

exit 0
