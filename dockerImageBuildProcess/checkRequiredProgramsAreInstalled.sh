#!/bin/bash

if ! [ -d ${DOCKJOB_GITROOT}/app/test ]; then
  echo "Couldn't find ${DOCKJOB_GITROOT}/app/test location - are you running this script from the correct path?"
  exit 1
fi

if ! [ -x "$(command -v ${CMD_PYTHONTEST})" ]; then
  echo "Error: ${CMD_PYTHONTEST} is not installed." >&2
  exit 1
fi

if ! [ -x "$(command -v ${CMD_NPM})" ]; then
  echo "Error: ${CMD_NPM} is not installed." >&2
  exit 1
fi

if ! [ -x "$(command -v ${CMD_CODECEPTJS})" ]; then
  echo "Error: ${CMD_CODECEPTJS} is not installed." >&2
  exit 1
fi

if ! [ -x "$(command -v ${CMD_QUASAR})" ]; then
  echo "Error: ${CMD_QUASAR} is not installed." >&2
  exit 1
fi

if ! [ -x "$(command -v ${CMD_DOCKER})" ]; then
  echo "Error: ${CMD_DOCKER} is not installed." >&2
  exit 1
fi

if ! [ -x "$(command -v ${CMD_GIT})" ]; then
  echo "Error: ${CMD_GIT} is not installed." >&2
  exit 1
fi

exit 0

