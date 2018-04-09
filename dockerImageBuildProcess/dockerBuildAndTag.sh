#!/bin/bash

source ./setEnviroment.sh

echo "Executing docker build"

DOCKER_USERNAME=metcarob
DOCKER_IMAGENAME=dockjob
cd ${DOCKJOB_GITROOT}

echo "Ensuring there are no local changes"
if [[ `${CMD_GIT} status --porcelain` ]]; then
  echo ""
  echo "Error - there are local changes commit these before continuing"
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

VERSIONFILE=${DOCKJOB_GITROOT}/VERSION
cd ${START_DIR}
./bumpVersion.sh ${VERSIONFILE}
RES=$?
if [ ${RES} -ne 0 ]; then
  cd ${START_DIR}
  echo ""
  echo "Bump version failed"
  exit 1
fi
VERSIONNUM=$(cat ${VERSIONFILE})

# must build AFTER the version is bumped as the version file is imported to the image
cd ${DOCKJOB_GITROOT}
eval ${CMD_DOCKER} build . -t ${DOCKER_USERNAME}/${DOCKER_IMAGENAME}:latest
RES=$?
if [ ${RES} -ne 0 ]; then
  cd ${START_DIR}
  echo ""
  echo "Docker build failed"
  exit 1
fi

cd ${DOCKJOB_GITROOT}
${CMD_GIT} add -A
${CMD_GIT} commit -m "version ${VERSIONNUM}"
${CMD_GIT} tag -a "${VERSIONNUM}" -m "version ${VERSIONNUM}"
${CMD_GIT} push
${CMD_GIT} push --tags
${CMD_DOCKER} tag ${DOCKER_USERNAME}/${DOCKER_IMAGENAME}:latest ${DOCKER_USERNAME}/${DOCKER_IMAGENAME}:${VERSIONNUM}

# push it
#${CMD_DOCKER} push ${DOCKER_USERNAME}/${DOCKER_IMAGENAME}:latest
#${CMD_DOCKER} push ${DOCKER_USERNAME}/${DOCKER_IMAGENAME}:${VERSIONNUM}


echo "Script Complete"

cd ${START_DIR}
exit 0
