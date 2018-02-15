from flask import Flask, Blueprint, jsonify, request
from flasgger import Swagger
from api import app
import signal
import sys
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
  expectedNumberOfParams = 6
  if (len(sys.argv) != expectedNumberOfParams):
    raise Exception('Wrong number of paramaters passed (Got ' + str(len(sys.argv)) + " expected " + str(expectedNumberOfParams) + ")")
  arg_mode = sys.argv[1]
  arg_version = sys.argv[2]
  arg_frontend = sys.argv[3]
  arg_apiurl = sys.argv[4]
  arg_apiaccesssecurity = sys.argv[5]
  GlobalParamaters.set(GlobalParamatersClass(arg_mode, arg_version, arg_frontend, arg_apiurl, arg_apiaccesssecurity))
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
      "version": arg_version
    },
    "host": arg_apiurl,  # overrides localhost:500
    "basePath": "",  # base bash for blueprint registration
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

