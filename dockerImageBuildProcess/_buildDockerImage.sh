#!/bin/bash

source ./setEnviroment.sh

cd ${START_DIR}
./checkRequiredProgramsAreInstalled.sh
RES=$?
if [ ${RES} -ne 0 ]; then
  cd ${START_DIR}
  exit 1
fi

cd ${DOCKJOB_GITROOT}
echo "Ensuring there are no local changes"
if [[ `${CMD_GIT} status --porcelain` ]]; then
  echo ""
  echo "Error - there are local changes commit these before continuing"
  exit 1
fi

cd ${START_DIR}
./runAllTests.sh
RES=$?
if [ ${RES} -ne 0 ]; then
  cd ${START_DIR}
  exit 1
fi

echo "Executing Quasar webfrontend build"
cd ${DOCKJOB_GITROOT}/webfrontend
eval ${CMD_QUASAR} build
RES=$?
if [ ${RES} -ne 0 ]; then
  cd ${START_DIR}
  echo ""
  echo "Quasar build failed"
  exit 1
fi

cd ${START_DIR}
./dockerBuildAndTag.sh
RES=$?
if [ ${RES} -ne 0 ]; then
  cd ${START_DIR}
  exit 1
fi

exit 0

