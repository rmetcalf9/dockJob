#!/bin/bash
echo "Runs delete job test mutiple times to catch intermatiant failure"

while [ 1 = 1 ]
do
  sudo nosetests --rednose ./test/test_jobsDataAPI.py:test_jobsData.test_deleteJobRemovedExecutionLogs
  echo "complete"
  # need to sleep to give ctl+c a chance to work
  sleep 1
done
