#!/bin/bash

echo 'Inserting Example Jobs'

for i in `seq 0 59`;
do
  TN=$(printf "%03d" ${i})
  JSON="{    \"enabled\": true,    \"name\": \"Test ${TN}\",    \"repetitionInterval\": \"HOURLY:${i}\",    \"command\": \"echo Running Test ${TN}\necho Finished\"  }"
  curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d "${JSON}" 'http://127.0.0.1:80/api/jobs/'
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


