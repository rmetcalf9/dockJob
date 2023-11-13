#! /usr/bin/env bash

source ./_repo_vars.sh

TAG=${BUILD_IMAGE_NAME_AND_TAG}
if [ $# -ne 0 ]; then
  TAG=${1}
  echo "Tag provided: ${TAG}"
fi


echo "Building project ${PROJECT_NAME} to image ${TAG}"

docker build \
  -t ${BUILD_IMAGE_NAME_AND_TAG} \
  --build-arg RJM_BUILDQUASARAPP_IMAGE=${RJM_BUILDQUASARAPP_IMAGE} \
  --build-arg RJM_VERSION=local \
  .
BUILD_RES=$?
if [[ ${BUILD_RES} -ne 0 ]]; then
  echo "Build failed - ${BUILD_RES}"
  exit 1
fi

exit 0
