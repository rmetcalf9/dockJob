from flask import Flask
from api import app
import signal
import sys
from GlobalParamaters import GlobalParamaters, GlobalParamatersClass

#Development code required to allow all access
# TODO make this dev only and runnable on an option
@app.after_request
def after_request(response):
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
  expectedNumberOfParams = 4
  if (len(sys.argv) != expectedNumberOfParams):
    raise Exception('Wrong number of paramaters passed (Got ' + str(len(sys.argv)) + " expected " + str(expectedNumberOfParams) + ")")
  arg_mode = sys.argv[1]
  arg_version = sys.argv[2]
  arg_frontend = sys.argv[3]
  GlobalParamaters = GlobalParamatersClass(arg_mode, arg_version, arg_frontend)
  print(GlobalParamaters.getStartupOutput())
  app.run(host='0.0.0.0', port=80, debug=False)
except ServerTerminationError as e:
  print("Stopped")

