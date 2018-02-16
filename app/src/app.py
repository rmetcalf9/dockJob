from flask import Flask, Blueprint, jsonify, request
from flasgger import Swagger
from api import app
import signal
import sys
import os
from GlobalParamaters import GlobalParamaters, GlobalParamatersClass

#Development code required to add CORS allowance in developer mode
@app.after_request
def after_request(response):
  if (GlobalParamaters.get().getDeveloperMode()):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

#Code required to ensure that container will exit when a signal is received
class ServerTerminationError(Exception):
  def __init__(self):
    pass
  def __str__(self):
    return "Server Terminate Error"

def exit_gracefully(signum, frame):
  print("Exit Gracefully called")
  raise ServerTerminationError()

signal.signal(signal.SIGINT, exit_gracefully)
signal.signal(signal.SIGTERM, exit_gracefully) #sigterm is sent by docker stop command
try:
  expectedNumberOfParams = 0
  if ((len(sys.argv)-1) != expectedNumberOfParams):
    raise Exception('Wrong number of paramaters passed (Got ' + str((len(sys.argv)-1)) + " expected " + str(expectedNumberOfParams) + ")")
  GlobalParamaters.set(GlobalParamatersClass(os.environ))
  print(GlobalParamaters.get().getStartupOutput())

  # Make app support /apidocs for swaggerUI
  swaggerTemplate = {
    "swagger": "2.0",
    "info": {
      "title": "DockJob API",
      "description": "API for DockJob",
      "contact": {
        "responsibleOrganization": "ME",
        "responsibleDeveloper": "Me",
        # "email": "rmetcalf9@googlemail.com",
        "url": "https://github.com/rmetcalf9/dockJob",
      },
      "termsOfService": "http://me.com/terms",
      "version": GlobalParamaters.get().version
    },
    "host": GlobalParamaters.get().getAPIHost(),  # overrides localhost:500
    #basePath dosen't seem to be used for registering the blueprint, but it is used for internal links
    "basePath": GlobalParamaters.get().getAPIPath(),  # base bash for blueprint registration
    "schemes": [
      "http",
      "https"
    ]
  }
  swaggerConfig = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/apidocs/"
  }

  swagger = Swagger(app, template=swaggerTemplate, config=swaggerConfig)

  app.run(host='0.0.0.0', port=80, debug=False)
except ServerTerminationError as e:
  print("Stopped")

