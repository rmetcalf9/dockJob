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
#cd ${DOCKJOB_GITROOT}/webfrontend
#eval ${CMD_NPM} test
#RES=$?
#if [ ${RES} -ne 0 ]; then
#  echo ""
#  echo "Webfrontend unit tests failed"
#  exit 1
#fi
echo "Webfrontend unit tests skipped"

exit 0

