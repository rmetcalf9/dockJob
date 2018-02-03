# Architecture of DockJob

DockJob is designed to generate a single Docker image.

Inside the image are two seperate components. Firstly the app, this is a python flask aplication whith a service based API. The source and unit tests for this are located in the ./app directory. The second compoennt is the web frontend. This is a webapplication which uses the quasar framework. It's source and unit tests are located in the ./webfrontend directory.

When the image is running it will run the python flask application to provide the API's. It will also serve the javascript files for the quasar frontend.

API URL: http://host:80/dockjobapi/
Frontend URL: http://host:80/dockjobfrontend/

The full application is designed to run inside a docker stack fronted by an API gateway like Kong.

## Security

The API is protected by Kong using a username and password.
(Future plan is to implement a login endpoint and make this a jwt token.)

The dockjobfrontend is not protected by any security, however to operate it must access the API using the users username and password.



