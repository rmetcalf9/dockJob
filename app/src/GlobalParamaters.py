import os
import json
from urllib.parse import urlparse

invalidModeArgumentException = Exception('Invalid Mode Argument')
invalidFrontentPathArgumentException = Exception('Invalid Web Frontend Path Argument')
invalidVersionArgumentException = Exception('Invalid Version Argument')
invalidInvalidApiaccesssecurityException = Exception('Invalid API Access Security Argument')
invalidInvalidApiURLException = Exception('Invalid API URL Argument')

# class to store GlobalParmaters
class GlobalParamatersClass():
  mode = None
  version = None
  webfrontendpath = None
  apiurl = None
  apidocsurl = None
  apiaccesssecurity = None
  
  #Read environment variable or raise an exception if it is missing and there is no default
  def readFromEnviroment(self, env, envVarName, defaultValue, exceptionToRaiseIfInvalid, acceptableValues):
    try:
      val = env[envVarName]
      if (acceptableValues != None):
        if (val not in acceptableValues):
          raise exceptionToRaiseIfInvalid
      return val
    except KeyError:
      if (defaultValue == None):
        raise exceptionToRaiseIfInvalid
      return defaultValue
  
  def __init__(self, env):
    self.mode = self.readFromEnviroment(env, 'APIAPP_MODE', None, invalidModeArgumentException, ['DEVELOPER','DOCKER'])
    self.version = self.readFromEnviroment(env, 'APIAPP_VERSION', None, invalidVersionArgumentException, None)
    self.webfrontendpath = self.readFromEnviroment(env, 'APIAPP_FRONTEND', None, invalidFrontentPathArgumentException, None)
    self.apiurl = self.readFromEnviroment(env, 'APIAPP_APIURL', None, invalidInvalidApiURLException, None)
    self.apidocsurl = self.readFromEnviroment(env, 'APIAPP_APIDOCSURL', '_', invalidInvalidApiURLException, None)
    apiaccesssecuritySTR = self.readFromEnviroment(env, 'APIAPP_APIACCESSSECURITY', None, invalidInvalidApiaccesssecurityException, None)

    if (self.webfrontendpath != '_'):
      if (not os.path.isdir(self.webfrontendpath)):
        raise invalidFrontentPathArgumentException
    if (len(self.version) == 0):
      raise invalidVersionArgumentException

    try:
      self.apiaccesssecurity = json.loads(apiaccesssecuritySTR)
    except json.decoder.JSONDecodeError:
      print('Invalid JSON for apiaccesssecurity - ' + apiaccesssecuritySTR)
      raise invalidInvalidApiaccesssecurityException

  def getStartupOutput(self):
    r = 'Mode:' + self.mode + '\n'
    r += 'Version:' + self.version + '\n'
    r += 'Frontend Location:' + self.webfrontendpath + '\n'
    r += 'apiurl:' + self.apiurl + '\n'
    r += 'apidocsurl:' + self.apidocsurl + '\n'
    r += 'apiaccesssecurity:' + json.dumps(self.apiaccesssecurity) + '\n'
    return r

  def getDeveloperMode(self):
    return (self.mode == 'DEVELOPER')

  def getWebFrontendPath(self):
    return self.webfrontendpath

  def getWebServerInfoJSON(self):
    return json.dumps({'version': self.version,'apiurl': self.apiurl,'apidocsurl': self.apidocsurl,'apiaccesssecurity': self.apiaccesssecurity})

  def getAPIHost(self):
    return urlparse(self.apiurl).netloc

  def getSanitizedPath(self, url):
    a = urlparse(url).path.strip()
    if (a[-1:] == '/'):
      a = a[:-1]
    return a

  def getAPIPath(self):
    return self.getSanitizedPath(self.apiurl)

  def overrideAPIDOCSPath(self):
    return (self.getAPIDOCSPath() != '')

  def getAPIDOCSPath(self):
    return self.getSanitizedPath(self.apidocsurl)


