# Test Driven Development

I am using this project to learn and practice Test Driven Development methods. I am aiming to use a quaterly cycle where I plan features, a weekly cycle where I write integration tests and a daily cycle where I use TDD to generate unit tests and the code for the project. This page describes the setup for each of the tests.

## Testing

### Integration Tests

These tests are kept in /integrationtests

I have used (http://codecept.io/quickstart/) to create the tests here. To run the tests

1. Start a Standalone Selenium server. I am using the Webdriver and the server should support at least one browser
2. In the integration directory run "codeceptjs run --steps"

### API Unit Tests

The API is a flask app and unit tests can be run continously during development. To do this goto the app directory and run the script continous_test.sh

### Frontend Unit Tests

TODO


## Build Process

TODO I will document my full build process which generates the docker image here

