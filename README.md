# DockJob

Job schedular with a web UI - designed to run as a container. I am creating this project to build myself a small light weight job schedular. I needed this because I am building a docker stack and I want to run a schedular inside the stack to replace the use of cron. My searches for alternatives (https://github.com/jjethwa/rundeck/issues/101) have hit a deadend, so I thought I would put together a simple API based python application.

 - Works in any web context
 - Works from any port
 - No https (Designed to run behind Kong or simular reverse proxy)
 - No security (Provided by reverse proxy)
 - Main interface is a simple json api
 - UI developed which connects to api.
 - Will run any command inside the container - but I am really wanting to run wget commands
 - Keeps logs of recent runs of jobs.
 - INITIALLY won't use a data store as a backend. On restart will lose all data, configured jobs, logs, etc.
 - 'Run now' button as well as schedulad run


# Road map

 - Set up project
 - Package API into container
 - Design API
 - Get API MVP working
 - Design UI
 - Get UI MVP working

# Links
[Description of Architecture](ARCHITECTUREURE.md)

# TODO Running instructions (docker compose file)

# Running just the backend server

````
sudo python3 ./app/src/app.py
````


