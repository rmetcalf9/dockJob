#! /usr/bin/env bash

source ./_repo_vars.sh

echo "Running project ${PROJECT_NAME}  (Tag=${BUILD_IMAGE_NAME_AND_TAG})"
echo " - You can get to the API with: curl superego:8301/api/serverinfo"
echo " - You can get to the frontend with: curl superego:8301/frontend/"


docker run --rm -it \
  -p 8301:80 \
  --name ${PROJECT_NAME} \
  --env APIAPP_APIURL=http://localhost:8301/api \
  --env APIAPP_APIDOCSURL=http://localhost:8301/apidocs \
  --env APIAPP_FRONTENDURL=http://localhost:8301/frontend \
  --env APIAPP_COMMON_ACCESSCONTROLALLOWORIGIN="http://localhost:8301,http://superego:8301" \
  ${BUILD_IMAGE_NAME_AND_TAG}
RUN_RES=$?
if [[ ${RUN_RES} -ne 0 ]]; then
  echo "Run failed ${RUN_RES}"
  exit 1
fi

exit 0
