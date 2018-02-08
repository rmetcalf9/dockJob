#!/bin/bash

#Check the input paramaters are correct
if [[ $# != 1 ]]
then
  echo "ERROR - Must be called with one parameter"
  exit 1
fi

VERSION_FILE=${1}
if [[ ! -e ${VERSION_FILE} ]]; then
  echo "ERROR - Couldn't find version file"
  exit 1
fi


echo "Bump version"
#Find minor version - text AFTER last dot in version string
OLDVERSION=$(cat ${VERSION_FILE})
OLDMINORVERSION=$(echo ${OLDVERSION} | sed 's/.*\.//')
CHARSINFIRSTPART=$(expr ${#OLDVERSION} - ${#OLDMINORVERSION})
RES=$?
if [ ${RES} -ne 0 ]; then
  echo "Invalid version number"
  exit 1
fi
OLDVERSIONWITHOUTMINOR=${OLDVERSION:0:${CHARSINFIRSTPART}}
RES=$?
if [ ${RES} -ne 0 ]; then
  echo "Invalid version number (Can't get first part)"
  exit 1
fi
NEWVERSION=${OLDVERSIONWITHOUTMINOR}$(expr ${OLDMINORVERSION} + 1)
echo "Old Version: ${OLDVERSION}"
echo "New Version: ${NEWVERSION}"

echo ${NEWVERSION} > ${VERSION_FILE}

exit 0