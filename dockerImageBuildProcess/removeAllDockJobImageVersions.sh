#!/bin/bash

source ./setEnviroment.sh

# Script designed to remove all local dockjob images

#TODO Alter this code so it removes only metcarob/dockjob images

docker system prune -a -f
RES=$?
if [ ${RES} -ne 0 ]; then
  cd ${START_DIR}
  echo 'ERROR'
  exit 1
fi

exit 0

