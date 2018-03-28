# Docker Image Build Process

This directory contains a set of bash scripts which build the docker image.

## Image build process

To build an image I have a process that runs all the unit and integration tests, then builds and tags the image.

Follow steps [here](../integrationtests/README.md) to ensure the integrations tests will work. (You don't need to run step 4)

Run the script _buildDockerImage.sh (you need to sudo this as the tests require root access to run. This is because dockjob runs jobs as different users.)

Once done a freshly tagged image should be produced
