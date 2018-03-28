# Compose Exmaples

As Dockjob is designed to be run as part of a ‘docker stack’ with Kong in front of it providing https and user accounts I have provided this section with a set of examples showing how it could be run. These examples should be run on a machine with a docker environment which is set up in a swarm. The commands should be run from a directory with the relevant .yml file.

# Docker compose Standalone
This uses docker to run dockjob standalone on a machine. This example shows setting dockjob options via environment variables. You must change the urls in docker-compose-standalone.yml replacing the host name with the hostname clients need to use to access dockjob.
Command to run:
````
docker stack deploy --compose-file=docker-compose-standalone.yml dockjob-standalone
````

When done use 
````
docker stack rm dockjob-standalone
````
to halt the stack.


