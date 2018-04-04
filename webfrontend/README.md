# dockJob - Webfrontend

The webfrontend for docJob is a Quaser application http://quasar-framework.org/. It is designed to run on a users browser and connect to the application via webapi's.

## Development

To run a development instance first run a development instance of the application [see here](../app/README.md#running-development-instance)
Then use the standard quasar command to run a development instance of the frontend:
````
quasar dev
````

## Unit testing

I have used the [Jest Framework](https://facebook.github.io/jest/) for unit testing. This can be triggered by running
````
npm test
````
Tests are stored [here](./test)

## Key design points

### How the frontend discovers the API url

As the application is designed to be run behind a reverse proxy it must identify the correct url to use when calling the API. This process also needs to work when running the application in various development enviroments without a reverse proxy. To achieve this the webfrontend will try and get connection information from each of the following url's until it gets a valid response: [see src/webfrontendConnectionData.js](./src/webfrontendConnectionData.js]
 - webfrontendConnectionData
 - /webfrontendConnectionData
 - http://somefunnyhostname.com:5080/frontend/webfrontendConnectionData
 - http://localhost:80/frontend/webfrontendConnectionData

The response to this request will contain the API url which is then used. This enables the application to provide a response to the call or for it to be set by writing a special file into the applications directory.

### Security of the API

In development mode no login is required, but in other instances the applicaiton needs to add a security header to each API request. The response to the webfrontendConnectionData call will also contain a apiaccesssecurity field which will tell the applicaiton if it needs to prompt the user for a password to access the API.

## Useful links when using quasar

Icon Information - http://quasar-framework.org/components/icons.html

