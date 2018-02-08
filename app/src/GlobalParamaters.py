import os

invalidModeArgumentException = Exception('Invalid Mode Argument')
invalidFrontentPathArgumentException = Exception('Invalid Web Frontend Path Argument')
invalidVersionArgumentException = Exception('Invalid Version Argument')

# class to store GlobalParmaters
class GlobalParamatersClass():
  mode = None
  version = None
  webfrontendpath = None
  def __init__(self, mode, version, webfrontendpath):
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

  def getStartupOutput(self):
    r = 'Mode:' + self.mode + '\n'
    r += 'Version:' + self.version + '\n'
    r += 'Frontend Location:' + self.webfrontendpath + '\n'
    return r

GlobalParamaters = None
