import os
import json

invalidModeArgumentException = Exception('Invalid Mode Argument')
invalidFrontentPathArgumentException = Exception('Invalid Web Frontend Path Argument')
invalidVersionArgumentException = Exception('Invalid Version Argument')
invalidInvalidApiaccesssecurityException = Exception('Invalid API Access Security Argument')

# class to store GlobalParmaters
class GlobalParamatersClass():
  mode = None
  version = None
  webfrontendpath = None
  apiurl = None
  apiaccesssecurity = None
  def __init__(self, mode, version, webfrontendpath, apiurl, apiaccesssecurity):
    if (mode == 'DEVELOPER'):
      pass
    elif (mode == 'DOCKER'):
      pass
    else:
      raise invalidModeArgumentException
    if (webfrontendpath != '_'):
      if (not os.path.isdir(webfrontendpath)):
        raise invalidFrontentPathArgumentException
    if (len(version) == 0):
      raise invalidVersionArgumentException

    self.mode = mode
    self.version = version
    self.webfrontendpath = webfrontendpath
    self.apiurl = apiurl
    try:
      self.apiaccesssecurity = json.loads(apiaccesssecurity)
    except json.decoder.JSONDecodeError:
      print('Invalid JSON for apiaccesssecurity - ' + apiaccesssecurity)
      raise invalidInvalidApiaccesssecurityException

  def getStartupOutput(self):
    r = 'Mode:' + self.mode + '\n'
    r += 'Version:' + self.version + '\n'
    r += 'Frontend Location:' + self.webfrontendpath + '\n'
    r += 'apiurl:' + self.apiurl + '\n'
    r += 'apiaccesssecurity:' + json.dumps(self.apiaccesssecurity) + '\n'
    return r

  def getDeveloperMode(self):
    return (self.mode == 'DEVELOPER')

  def getWebFrontendPath(self):
    return self.webfrontendpath

  def getWebServerInfoJSON(self):
    print(self.apiaccesssecurity)
    return json.dumps({'version': self.version,'apiurl': self.apiurl,'apiaccesssecurity': self.apiaccesssecurity})

class GlobalParamatersPointerClass():
  obj = None
  def set(self, obj):
    self.obj = obj
  def get(self):
    return self.obj

GlobalParamaters = GlobalParamatersPointerClass()
