#!/bin/bash


START_DIR=$(pwd)
DOCKER_USERNAME=metcarob
DOCKER_IMAGENAME=dockjob

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

echo "Execuring Quasar webfrontend build"
cd ${DOCKJOB_GITROOT}/webfrontend
eval ${CMD_QUASAR} build
RES=$?
if [ ${RES} -ne 0 ]; then
  cd ${START_DIR}
  echo ""
  echo "Quasar build failed"
  exit 1
fi

echo "Executing docker build"
cd ${DOCKJOB_GITROOT}

echo "Ensuring there are no local changes"
if [[ `${CMD_GIT} status --porcelain` ]]; then
  echo ""
  echo "Error - there are local changes commit these before continuing"
  exit 1
fi

echo "Bump version"
${CMD_DOCKER} run --rm -v "$PWD":/app treeder/bump patch
RES=$?
if [ ${RES} -ne 0 ]; then
  cd ${START_DIR}
  echo ""
  echo "Bump version failed"
  exit 1
fi
version=`cat VERSION`
echo "version: $version"



eval ${CMD_DOCKER} build . -t ${DOCKER_USERNAME}/${DOCKER_IMAGENAME}:latest
RES=$?
if [ ${RES} -ne 0 ]; then
  cd ${START_DIR}
  echo ""
  echo "Docker build failed"
  exit 1
fi

${CMD_GIT} add -A
${CMD_GIT} commit -m "version $version"
${CMD_GIT} tag -a "$version" -m "version $version"
${CMD_GIT} push
${CMD_GIT} push --tags
docker tag ${DOCKER_USERNAME}/${DOCKER_IMAGENAME}:latest ${DOCKER_USERNAME}/${DOCKER_IMAGENAME}:$version

# push it
#${CMD_DOCKER} push ${DOCKER_USERNAME}/${DOCKER_IMAGENAME}:latest
#${CMD_DOCKER} push ${DOCKER_USERNAME}/${DOCKER_IMAGENAME}:$version


echo "Script Complete"

cd ${START_DIR}
exit 0

