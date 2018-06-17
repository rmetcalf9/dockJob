#!/bin/bash

echo 'Inserting Example Jobs'

for i in `seq 0 59`;
do
  TN=$(printf "%03d" ${i})
  JSON="{    \"enabled\": true,    \"name\": \"Test ${TN}\",    \"repetitionInterval\": \"HOURLY:${i}\",    \"command\": \"echo Running Test ${TN}\necho Finished\",  \"pinned\": true  }"
  curl --fail -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d "${JSON}" 'http://127.0.0.1:80/api/jobs/'
  RES=$?
  echo $RES
  if [[ ${RES} -ne 0 ]]; then
    echo "Failed with result ${RES}"
    echo "Post JSON was: ${JSON}"
    exit 1
  fi
done

echo 'Inserting Example Job for Executions'


JSON="{    \"enabled\": false,    \"name\": \"Job With Executions\",    \"repetitionInterval\": \"\",    \"command\": \"ls -la\"  }"

JWEGUID=$(curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d "${JSON}" 'http://127.0.0.1:80/api/jobs/' | \
    python -c "import sys, json; print json.load(sys.stdin)['guid']")

echo "GUID for test executions: ${JWEGUID}"
for i in `seq 0 12`;
do
  TN=$(printf "%03d" ${i})
  JSON="{    \"name\": \"TestExecution ${TN}\"  }"
  curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d "${JSON}" "http://127.0.0.1:80/api/jobs/${JWEGUID}/execution"
done

exit 0

