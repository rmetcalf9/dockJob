#!/bin/bash

source ./setEnviroment.sh

# Script designed to remove all local dockjob images

ii=$(docker images | grep metcarob/dockjob)
if [ 0 -eq ${#ii} ]; then
  echo 'No metcarob/dockjob images present'
  exit 0
fi

docker images -a | grep "metcarob/dockjob" | awk '{print $3}' | xargs docker rmi -f
#docker system prune -a -f
RES=$?
if [ ${RES} -ne 0 ]; then
  cd ${START_DIR}
  echo 'ERROR'
  exit 1
fi

ii=$(docker images | grep metcarob/dockjob)
if [ 0 -ne ${#ii} ]; then
  echo 'Error metcarob/dockjob images remain'
  exit 1
fi

echo 'completed sucessfully'

exit 0

