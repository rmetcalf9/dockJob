#!/bin/bash
#Builds a local dev only image

source ./setEnviroment.sh

cd ${START_DIR}
./checkRequiredProgramsAreInstalled.sh
RES=$?
if [ ${RES} -ne 0 ]; then
  cd ${START_DIR}
  exit 1
fi

cd ${START_DIR}
####./runUnitTests.sh
####RES=$?
echo "SKIPPING UNIT TESTS"
if [ ${RES} -ne 0 ]; then
  cd ${START_DIR}
  exit 1
fi

echo "Executing Quasar webfrontend build"
cd ${DOCKJOB_GITROOT}/webfrontend
if [ -d ./dist ]; then
  rm -rf dist
fi
if [ -d ./dist ]; then
  echo "ERROR - failed to delete dist directory"
  cd ${START_DIR}
  exit 1
fi
eval ${CMD_QUASAR} build
RES=$?
if [ ${RES} -ne 0 ]; then
  cd ${START_DIR}
  echo ""
  echo "Quasar build failed"
  exit 1
fi
if [ ! -d ./dist ]; then
  echo "ERROR - build command didn't create webfrontend/dist directory"
  cd ${START_DIR}
  exit 1
fi

cd ${DOCKJOB_GITROOT}
eval ${CMD_DOCKER} build . -t dockjobdev:latest
RES=$?
if [ ${RES} -ne 0 ]; then
  cd ${START_DIR}
  echo ""
  echo "Docker build failed"
  exit 1
fi


echo "**********************************************************"
echo "**********************************************************"
echo "** DEVELOPMENT DOCKER IMAGE BUILD COMPLETED SUCESSfUlLY **"
echo "**********************************************************"
echo "**********************************************************"

echo "docker run -d -p 80:80 -e APIAPP_APIURL='http://cat-sdts.metcarob-home.com:80/api' -e'APIAPP_APIDOCSURL=http://cat-sdts.metcarob-home.com:80/apidocs' dockjobdev"

exit 0

