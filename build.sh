#! /usr/bin/env bash

source ./_repo_vars.sh

TAG=${BUILD_IMAGE_NAME_AND_TAG}
VERSION="local"
if [ $# -ne 0 ]; then
  TAG=${1}
  VERSION=${2}
  echo "Tag provided: ${TAG}"
  echo "Version provided: ${VERSION}"
fi


echo "Building project ${PROJECT_NAME} to image ${TAG}"

docker build \
  -t ${TAG} \
  --build-arg RJM_BUILDQUASARAPP_IMAGE=${RJM_BUILDQUASARAPP_IMAGE} \
  --build-arg RJM_VERSION=${VERSION} \
  .
BUILD_RES=$?
if [[ ${BUILD_RES} -ne 0 ]]; then
  echo "Build failed - ${BUILD_RES}"
  exit 1
fi

exit 0
