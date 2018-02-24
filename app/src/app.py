from appObj import appObj

import sys
import os

##App will host content in the following paths:
## /api        API
## /apidocs    API Documentation including swagger.json and swaggerUI
## /frontend   Frontend for this application
##

appObj.init(os.environ)

expectedNumberOfParams = 0
if ((len(sys.argv)-1) != expectedNumberOfParams):
  raise Exception('Wrong number of paramaters passed (Got ' + str((len(sys.argv)-1)) + " expected " + str(expectedNumberOfParams) + ")")

appObj.run()

