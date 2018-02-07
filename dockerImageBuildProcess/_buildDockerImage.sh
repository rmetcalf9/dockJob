#!/bin/bash


START_DIR=$(pwd)

source ./setEnviroment.sh

./checkRequiredProgramsAreInstalled.sh
RES=$?
if [ ${RES} -ne 0 ]; then
  cd ${START_DIR}
  exit 1
fi

./runAllTests.sh
RES=$?
if [ ${RES} -ne 0 ]; then
  cd ${START_DIR}
  exit 1
fi


echo "TODO rest of script"

cd ${START_DIR}
exit 0

