#!/bin/bash

export START_DIR=$(pwd)
cd ${START_DIR}
cd ../
export DOCKJOB_GITROOT=$(pwd)

cd ${START_DIR}
export CMD_PYTHONTEST="python3 -m pytest"
##TODO check rednose is installed
export CMD_NPM=npm
export CMD_CODECEPTJS=codeceptjs
export CMD_QUASAR=quasar
export CMD_DOCKER=docker
export CMD_GIT=git

