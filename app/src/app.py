from flask import Flask, Blueprint, jsonify, request
from appObj import appObj
appObj.init()

from api import t

from flask_restplus import Api, Resource, fields
import signal
import sys
import os
from GlobalParamaters import GlobalParamaters, GlobalParamatersClass

##App will host content in the following paths:
## /api        API
## /apidocs    API Documentation including swagger.json and swaggerUI
## /frontend   Frontend for this application
##

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

  appObj.run()
except ServerTerminationError as e:
  print("Stopped")

