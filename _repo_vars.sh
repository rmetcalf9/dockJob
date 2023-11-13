#!/bin/bash

#export PYTHON_IMAGE=python:3.11.3
export PROJECT_NAME=${PWD##*/}          # to assign to a variable
export PROJECT_NAME=${PROJECT_NAME:-/}
export BUILD_IMAGE_NAME_AND_TAG=${PROJECT_NAME}_build_image:local

export RJM_BUILDQUASARAPP_IMAGE="metcarob/docker-build-quasar-app:0.0.30"
