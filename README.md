# DockJob

Job schedular with a web UI - designed to run inside a container. I am creating this project to build myself a small light weight job schedular. I need this because I am building a docker stack and I want to run a schedular inside the stack to replace the use of cron. My searches for alternatives (https://github.com/jjethwa/rundeck/issues/101) have hit a deadend, so I thought I would put together a simple API based python application.

 - Doesn't do https or security itself - [Kong](https://konghq.com/) will also be deployed to the stack to provide this
 - Works in any web context
 - Works from any port
 - Main interface is a simple json api
 - UI developed which connects to api.
 - Will run any command inside the container - but I am really focused to run wget commands. This makes use of security provided by docker networking.
 - Keeps logs of recent runs of jobs.
 - INITIALLY won't use a data store as a backend. On restart will lose all data, configured jobs, logs, etc.
 - 'Run now' button as well as scheduled run


# Road map

 - Set up project DONE
 - Package API into container DONE
 - Design API
 - Get API MVP working
 - Design UI
 - Get UI MVP working

# Running dockJob

TODO Notes on how to run
 

# Helping me develop dockJob

A high level [description of the architecture is here](ARCHITECTURE.md).

I have tried to organize the project logically into sub directories and README.md files explain each component:
| Component         | Location                  | Description                                                                                                                                              |
|-------------------|---------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| [Application](./app/README.md)       | ./app                     | DockJob Application that runs continuously. This provides a RESTFUL API and executes the Jobs as scheduled, or on receiptof an API call.                 |
| [Webfrontend](./webfrontend/README.md)       | ./webfrontend             | Web application that is run on browsers and will talk to the Application to provide a graphical UI.                                                      |
| [Integration tests](./integrationtests/README.md) | ./integrationtests        | Set of tests which test both the Application and Webfrontend                                                                                             |
| [Build Process](./dockerImageBuildProcess/README.md)     | ./dockerImageBuildProcess | Bash scripts which run all tests (both unit and integration) and then versions and builds the docker image                                               |
| [Compose Examples](./composeExamples/README.md)  | ./composeExamples         | The image is designed to work in a docker swarm with Kong as a reverse proxy to provide security. This directory provides some examples of deploying it. |

# TODO Running instructions (docker compose file)


