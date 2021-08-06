#!/bin/bash

if [ -d "./app" ]; then
  echo "Changing into app directory"
  cd ./app
fi

sudo ./continous_test.sh $@
