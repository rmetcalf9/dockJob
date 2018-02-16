from flask import Flask, Blueprint, jsonify, request
from api import app
from flask_restplus import Api, Resource, fields
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

  #app.config['SERVER_NAME'] = 'servername:123'
  app.run(host='0.0.0.0', port=80, debug=False)
except ServerTerminationError as e:
  print("Stopped")

