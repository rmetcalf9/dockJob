# DockJob Application

This is a python application based on Flask. It provides an API which can be used to control the application.

# Running the application


# Development

## Required Setup

python3 must be installed (with pip).
Requirements are listed in [./src/requirments.txt](./src/requirments.txt) to install these run the following from the app directory:
````
sudo pip3 install -r ./src/requirments.txt
````

## Developing

I use a TDD approach to develop this application. I always start with integration tests [../integrationtests/README.md](../integrationtests/README.md).

Unit tests for the application are based on nosetests. (You must have nosetests and rednose installed to run these.)
The following command will run unit tests and wait for any file to change then re-run them:
````
./continous_test.sh
````

## Running  Development-Instance

As well as running in testing mode the python application can be run outside of the docker container. As it relies on enviroment variables to be set some bash scripts are included to help with this.

For most developers the following script will run a local instance:
````
sudo run_app_developer.sh
````

If the development instance is inside a virtual machine then run_app_developer_workClient.sh may help as it sets the connection URL's and ports to different values.
