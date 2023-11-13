#!/bin/bash

echo "This script launches all the components on a development machine"

if [[ $(whoami) != 'root' ]]; then
  echo "Must run as root"
  exit 1
fi

TR=./run_app_developer.sh
if [[ $# -eq 1 ]]; then
  if [[ E${1} == 'Ewc' ]]; then
    TR=./run_app_developer_workClient.sh
  else
    echo "Option must be wc or nothing"
    exit 1
  fi
fi


tmux \
  new-session  "cd ./app ; ${TR}" \; \
  split-window "cd ./frontend ; quasar dev" \; \
  select-layout main-horizontal \; \
  select-pane -t 0 \; \
  split-window "cd ./app ; ./insert_example_jobs.sh"

exit 0
