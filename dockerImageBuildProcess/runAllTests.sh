#!/bin/bash

cd ${START_DIR}
./runUnitTests.sh
RES=$?
if [ ${RES} -ne 0 ]; then
  cd ${START_DIR}
  exit 1
fi


echo "Running integration tests"
#cd ${DOCKJOB_GITROOT}/integrationtests
#eval ${CMD_CODECEPTJS} run
#RES=$?
#if [ ${RES} -ne 0 ]; then
#  echo ""
#  echo "Integration tests failed - all of Selinum, python app and web frontend all running?"
#  exit 1
#fi
echo " Frontend tests disabled"



exit 0

