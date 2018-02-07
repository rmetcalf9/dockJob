#!/bin/bash

echo "Running python app unit tests"
cd ${DOCKJOB_GITROOT}/app
eval ${CMD_PYTHONTEST} ./test
RES=$?
if [ ${RES} -ne 0 ]; then
  echo ""
  echo "Python app unit tests failed"
  exit 1
fi

echo "Running webfrontend unit tests"
cd ${DOCKJOB_GITROOT}/webfrontend
eval ${CMD_NPM} test
RES=$?
if [ ${RES} -ne 0 ]; then
  echo ""
  echo "Webfrontend unit tests failed"
  exit 1
fi

echo "Running integration tests"
cd ${DOCKJOB_GITROOT}/integrationtests
eval ${CMD_CODECEPTJS} run
RES=$?
if [ ${RES} -ne 0 ]; then
  echo ""
  echo "Integration tests failed - all of Selinum, python app and web frontend all running?"
  exit 1
fi




exit 0

