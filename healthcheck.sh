#!/bin/bash

curl -f http://127.0.0.1:80/frontend/index.html?healthcheck=true
RES=$?
if [ ${RES} -ne 0 ]; then
  echo "healthcheck.sh - failed quasar index"
  exit 1
fi

curl -f http://127.0.0.1:80/api/serverinfo?healthcheck=true
RES=$?
if [ ${RES} -ne 0 ]; then
  echo "healthcheck.sh - failed python app"
  exit 1
fi

exit 0
