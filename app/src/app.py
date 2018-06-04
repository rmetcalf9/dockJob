from appObj import appObj

import sys
import os
import datetime
import pytz

##App will host content in the following paths:
## /api        API
## /apidocs    API Documentation including swagger.json and swaggerUI
## /frontend   Frontend for this application
##

curDatetime = datetime.datetime.now(pytz.utc)
appObj.init(os.environ, curDatetime)

try:
  uwsgi.atexit = appObj.exit_gracefully
except:
  print('uwsgi not availiable')

globalFlaskAppObj = appObj.flaskAppObject

if __name__ == "__main__":
  #Custom handler to allow me to use my own logger
  from werkzeug.serving import WSGIRequestHandler, _log

  class CustomRequestHandler(WSGIRequestHandler):
    # Stop logging sucessful health checks
    def log_request(self, code='-', size='-'):
      ignore = False
      if code > 199:
        if code < 300:
          if "healthcheck=true" in self.requestline:
            ignore = True

      if ignore:
        return
      return super(CustomRequestHandler, self).log_request(code,size)

  expectedNumberOfParams = 0
  if ((len(sys.argv)-1) != expectedNumberOfParams):
    raise Exception('Wrong number of paramaters passed (Got ' + str((len(sys.argv)-1)) + " expected " + str(expectedNumberOfParams) + ")")

  appObj.run(CustomRequestHandler)

