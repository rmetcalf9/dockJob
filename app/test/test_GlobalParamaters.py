from TestHelperSuperClass import testHelperSuperClass
from GlobalParamaters import GlobalParamatersClass, invalidModeArgumentException, invalidFrontentPathArgumentException, invalidVersionArgumentException, invalidInvalidApiaccesssecurityException
import json

class test_GlobalParamaters(testHelperSuperClass):

  def test_acceptDEVELOPERMode(self):
    gp = GlobalParamatersClass("DEVELOPER","TEST-1.2.3","_",'http://apiurl','[]')

  def test_acceptDOCKERMode(self):
    gp = GlobalParamatersClass("DOCKER","TEST-1.2.3","_",'http://apiurl','[]')

  def test_dontAcceptInvalidModeThrowsException(self):
    with self.assertRaises(Exception) as context:
      gp = GlobalParamatersClass("InvalidMode","TEST-1.2.3","_",'http://apiurl','[]')
    self.checkGotRightException(context,invalidModeArgumentException)

  def test_webservicepathDosentExistThrowsException(self):
    with self.assertRaises(Exception) as context:
      gp = GlobalParamatersClass("DOCKER","TEST-1.2.3","/a/b/c",'http://apiurl','[]')
    self.checkGotRightException(context,invalidFrontentPathArgumentException)

  def test_missingVersionThrowsException(self):
    with self.assertRaises(Exception) as context:
      gp = GlobalParamatersClass("DOCKER","","_",'http://apiurl','[]')
    self.checkGotRightException(context,invalidVersionArgumentException)

  def test_validWebFrontendDirectory(self):
    gp = GlobalParamatersClass("DOCKER","TEST-1.2.3","../app",'http://apiurl','[]')

  def test_startupOutput(self):
    gp = GlobalParamatersClass("DOCKER","TEST-1.2.3","../app",'http://apiurl','[]')
    self.assertEqual(gp.getStartupOutput(), 'Mode:DOCKER\nVersion:TEST-1.2.3\nFrontend Location:../app\napiurl:http://apiurl\napiaccesssecurity:[]\n')

  def test_developerMode(self):
    gp = GlobalParamatersClass("DOCKER","TEST-1.2.3","../app",'http://apiurl','[]')
    self.assertEqual(gp.getDeveloperMode(), False)
    gp = GlobalParamatersClass("DEVELOPER","TEST-1.2.3","../app",'http://apiurl','[]')
    self.assertEqual(gp.getDeveloperMode(), True)

  def test_getWebServerInfoNoAuth(self):
    expRes = json.dumps({
        'version': 'TEST-3.3.3', #// Version show as 0 fom this file
        'apiurl': 'http://apiurlxxx',
        'apiaccesssecurity': [] #// all supported auth types. Can be empty, or strings: basic-auth, jwt
        #// Empty list means no auth type
        #//  { type: basic-auth } - webfrontend will prompt user for username and password
        #//  ...
      })
    gp = GlobalParamatersClass("DOCKER","TEST-3.3.3","../app",'http://apiurlxxx','[]')
    self.assertJSONStringsEqual(gp.getWebServerInfoJSON(), expRes);

  def test_getWebServerInfoBasicAuth(self):
    expRes = json.dumps({
        'version': 'TEST-3.3.3', #// Version show as 0 fom this file
        'apiurl': 'http://apiurlxxx',
        'apiaccesssecurity': [{'type':'basic-auth'}] #// all supported auth types. Can be empty, or strings: basic-auth, jwt
        #// Empty list means no auth type
        #//  { type: basic-auth } - webfrontend will prompt user for username and password
        #//  ...
      })
    gp = GlobalParamatersClass("DOCKER","TEST-3.3.3","../app",'http://apiurlxxx','[{ "type": "basic-auth" }]')
    self.assertJSONStringsEqual(gp.getWebServerInfoJSON(), expRes);

  def test_invalidAPISecurityJSON(self):
    with self.assertRaises(Exception) as context:
      gp = GlobalParamatersClass("DOCKER","TEST-3.3.3","../app",'http://apiurlxxx','Some invalid JSON String')
    self.checkGotRightException(context,invalidInvalidApiaccesssecurityException)

