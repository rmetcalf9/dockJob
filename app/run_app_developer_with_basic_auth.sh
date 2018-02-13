#!/bin/bash

APP_DIR=.

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


python3 ./src/app.py "DEVELOPER" "DEVELOPMENT-${VERSION}" "_" "apirul_dosent_matter" "[\{'type': 'basic-auth' \}]" 
exit 0
