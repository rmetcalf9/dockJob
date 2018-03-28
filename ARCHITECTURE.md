# Architecture of DockJob

DockJob is designed to generate a single Docker image.

Inside the image are two seperate components. Firstly the app, this is a python flask aplication whith a service based API. The source and unit tests for this are located in the [./app](./app) directory. The second compoennt is the web frontend. This is a webapplication which uses the quasar framework. It's source and unit tests are located in the [./webfrontend](./webfrontend) directory.

When the image is running it will run the python flask application to provide the API's. It will also serve the javascript files for the quasar frontend. There is also a swagger UI endpoint which provides api documentation.

 - Frontend URL: http://host:80/frontend/
 - API URL: http://host:80/api/
 - API URL: http://host:80/apidocs/

The full application is designed to run inside a docker stack fronted by an API gateway like Kong. If required it is possible to seperate the webfrontend onto a seperate webserver.

## Security

The API is protected by Kong using a username and password.

The frontend is not protected by any security, however to operate it must access the API using the users username and password.

