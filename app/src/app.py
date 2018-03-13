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

expectedNumberOfParams = 0
if ((len(sys.argv)-1) != expectedNumberOfParams):
  raise Exception('Wrong number of paramaters passed (Got ' + str((len(sys.argv)-1)) + " expected " + str(expectedNumberOfParams) + ")")

appObj.run()

