# DockJob Application

This is a python application based on Flask. It provides an API which can be used to control the application.

# Running the application


# Development

## Required Setup

python3 must be installed (with pip).
Requirements are listed in [./src/requirments.txt] to install these run the following from the app directory:
````
pip install -r ./src/requirements.txt
````

## Developing

I use a TDD approach to develop this application. I always start with integration tests [../integrationtests/README.md].

Unit tests for the application are based on nosetests. (You must have nosetests and rednose installed to run these.)
The following command will run unit tests and wait for any file to change then re-run them:
````
./continous_test.sh
````

