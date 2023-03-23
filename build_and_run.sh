#! /usr/bin/env bash

docker build . -t localdevversion
BUILD_RES=$?
if [[ ${BUILD_RES} -ne 0 ]]; then
  echo "Build failed - ${BUILD_RES}"
  exit 1
fi

docker run --rm -it localdevversion
RUN_RES=$?
if [[ ${RUN_RES} -ne 0 ]]; then
  echo "Run failed ${RUN_RES}"
  exit 1
fi

exit 0
