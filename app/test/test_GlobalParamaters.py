from TestHelperSuperClass import testHelperSuperClass
from GlobalParamaters import GlobalParamatersClass, invalidModeArgumentException, invalidFrontentPathArgumentException, invalidVersionArgumentException, invalidInvalidApiaccesssecurityException
import json

class test_GlobalParamaters(testHelperSuperClass):

  def test_acceptDEVELOPERMode(self):
    env = {
      'APIAPP_MODE': 'DEVELOPER',
      'APIAPP_VERSION': 'TEST-1.2.3',
      'APIAPP_FRONTEND': '_',
      'APIAPP_APIURL': 'http://apiurl',
      'APIAPP_APIACCESSSECURITY': '[]',
    }
    gp = GlobalParamatersClass(env)

  def test_acceptDOCKERMode(self):
    env = {
      'APIAPP_MODE': 'DOCKER',
      'APIAPP_VERSION': 'TEST-1.2.3',
      'APIAPP_FRONTEND': '_',
      'APIAPP_APIURL': 'http://apiurl',
      'APIAPP_APIACCESSSECURITY': '[]',
    }
    gp = GlobalParamatersClass(env)

  def test_dontAcceptInvalidModeThrowsException(self):
    env = {
      'APIAPP_MODE': 'InvalidMode',
      'APIAPP_VERSION': 'TEST-1.2.3',
      'APIAPP_FRONTEND': '_',
      'APIAPP_APIURL': 'http://apiurl',
      'APIAPP_APIACCESSSECURITY': '[]',
    }
    with self.assertRaises(Exception) as context:
      gp = GlobalParamatersClass(env)
    self.checkGotRightException(context,invalidModeArgumentException)

  def test_webservicepathDosentExistThrowsException(self):
    env = {
      'APIAPP_MODE': 'DOCKER',
      'APIAPP_VERSION': 'TEST-1.2.3',
      'APIAPP_FRONTEND': '/a/b/c',
      'APIAPP_APIURL': 'http://apiurl',
      'APIAPP_APIACCESSSECURITY': '[]',
    }
    with self.assertRaises(Exception) as context:
      gp = GlobalParamatersClass(env)
    self.checkGotRightException(context,invalidFrontentPathArgumentException)

  def test_missingVersionThrowsException(self):
    env = {
      'APIAPP_MODE': 'DOCKER',
      'APIAPP_VERSION': '',
      'APIAPP_FRONTEND': '_',
      'APIAPP_APIURL': 'http://apiurl',
      'APIAPP_APIACCESSSECURITY': '[]',
    }
    with self.assertRaises(Exception) as context:
      gp = GlobalParamatersClass(env)
    self.checkGotRightException(context,invalidVersionArgumentException)

  def test_validWebFrontendDirectory(self):
    env = {
      'APIAPP_MODE': 'DOCKER',
      'APIAPP_VERSION': 'TEST-1.2.3',
      'APIAPP_FRONTEND': '../app',
      'APIAPP_APIURL': 'http://apiurl',
      'APIAPP_APIACCESSSECURITY': '[]',
    }
    gp = GlobalParamatersClass(env)

  def test_startupOutput(self):
    env = {
      'APIAPP_MODE': 'DOCKER',
      'APIAPP_VERSION': 'TEST-1.2.3',
      'APIAPP_FRONTEND': '../app',
      'APIAPP_APIURL': 'http://apiurl',
      'APIAPP_APIACCESSSECURITY': '[]',
    }
    gp = GlobalParamatersClass(env)
    self.assertEqual(gp.getStartupOutput(), 'Mode:DOCKER\nVersion:TEST-1.2.3\nFrontend Location:../app\napiurl:http://apiurl\napiaccesssecurity:[]\n')

  def test_developerMode(self):
    env = {
      'APIAPP_MODE': 'DOCKER',
      'APIAPP_VERSION': 'TEST-1.2.3',
      'APIAPP_FRONTEND': '../app',
      'APIAPP_APIURL': 'http://apiurl',
      'APIAPP_APIACCESSSECURITY': '[]',
    }
    gp = GlobalParamatersClass(env)
    self.assertEqual(gp.getDeveloperMode(), False)
    env = {
      'APIAPP_MODE': 'DEVELOPER',
      'APIAPP_VERSION': 'TEST-1.2.3',
      'APIAPP_FRONTEND': '../app',
      'APIAPP_APIURL': 'http://apiurl',
      'APIAPP_APIACCESSSECURITY': '[]',
    }
    gp = GlobalParamatersClass(env)
    self.assertEqual(gp.getDeveloperMode(), True)

  def test_getWebServerInfoNoAuth(self):
    env = {
      'APIAPP_MODE': 'DOCKER',
      'APIAPP_VERSION': 'TEST-3.3.3',
      'APIAPP_FRONTEND': '../app',
      'APIAPP_APIURL': 'http://apiurlxxx',
      'APIAPP_APIACCESSSECURITY': '[]',
    }
    expRes = json.dumps({
        'version': 'TEST-3.3.3', #// Version show as 0 fom this file
        'apiurl': 'http://apiurlxxx',
        'apiaccesssecurity': [] #// all supported auth types. Can be empty, or strings: basic-auth, jwt
        #// Empty list means no auth type
        #//  { type: basic-auth } - webfrontend will prompt user for username and password
        #//  ...
      })
    gp = GlobalParamatersClass(env)
    self.assertJSONStringsEqual(gp.getWebServerInfoJSON(), expRes);

  def test_getWebServerInfoBasicAuth(self):
    env = {
      'APIAPP_MODE': 'DOCKER',
      'APIAPP_VERSION': 'TEST-3.3.3',
      'APIAPP_FRONTEND': '../app',
      'APIAPP_APIURL': 'http://apiurlxxx',
      'APIAPP_APIACCESSSECURITY': '[{ "type": "basic-auth" }]',
    }
    expRes = json.dumps({
        'version': 'TEST-3.3.3', #// Version show as 0 fom this file
        'apiurl': 'http://apiurlxxx',
        'apiaccesssecurity': [{'type':'basic-auth'}] #// all supported auth types. Can be empty, or strings: basic-auth, jwt
        #// Empty list means no auth type
        #//  { type: basic-auth } - webfrontend will prompt user for username and password
        #//  ...
      })
    gp = GlobalParamatersClass(env)
    self.assertJSONStringsEqual(gp.getWebServerInfoJSON(), expRes);

  def test_invalidAPISecurityJSON(self):
    env = {
      'APIAPP_MODE': 'DOCKER',
      'APIAPP_VERSION': 'TEST-3.3.3',
      'APIAPP_FRONTEND': '../app',
      'APIAPP_APIURL': 'http://apiurlxxx',
      'APIAPP_APIACCESSSECURITY': 'Some invalid JSON String',
    }
    with self.assertRaises(Exception) as context:
      gp = GlobalParamatersClass(env)
    self.checkGotRightException(context,invalidInvalidApiaccesssecurityException)

