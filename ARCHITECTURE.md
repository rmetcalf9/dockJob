# Architecture of DockJob

DockJob is designed to generate a single Docker image.

Inside the image are two seperate components. Firstly the app, this is a python flask aplication whith a service based API. The source and unit tests for this are located in the ./app directory. The second compoennt is the web frontend. This is a webapplication which uses the quasar framework. It's source and unit tests are located in the ./webfrontend directory.

When the image is running it will run the python flask application to provide the API's. It will also serve the javascript files for the quasar frontend.

API URL: TODO
Frontend URL: TODO

The full application is designed to run inside a docker stack fronted by an API gateway like Kong.


