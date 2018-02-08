from TestHelperSuperClass import testHelperSuperClass
from GlobalParamaters import GlobalParamatersClass, invalidModeArgumentException, invalidFrontentPathArgumentException, invalidVersionArgumentException

class test_GlobalParamaters(testHelperSuperClass):

  def test_acceptDEVELOPERMode(self):
    gp = GlobalParamatersClass("DEVELOPER","TEST-1.2.3","_")

  def test_acceptDOCKERMode(self):
    gp = GlobalParamatersClass("DOCKER","TEST-1.2.3","_")

  def test_dontAcceptInvalidModeThrowsException(self):
    with self.assertRaises(Exception) as context:
      gp = GlobalParamatersClass("InvalidMode","TEST-1.2.3","_")
    self.checkGotRightException(context,invalidModeArgumentException)

  def test_webservicepathDosentExistThrowsException(self):
    with self.assertRaises(Exception) as context:
      gp = GlobalParamatersClass("DOCKER","TEST-1.2.3","/a/b/c")
    self.checkGotRightException(context,invalidFrontentPathArgumentException)

  def test_missingVersionThrowsException(self):
    with self.assertRaises(Exception) as context:
      gp = GlobalParamatersClass("DOCKER","","_")
    self.checkGotRightException(context,invalidVersionArgumentException)

  def test_validWebFrontendDirectory(self):
    gp = GlobalParamatersClass("DOCKER","TEST-1.2.3","../app")

  def test_startupOutput(self):
    gp = GlobalParamatersClass("DOCKER","TEST-1.2.3","../app")
    self.assertEqual(gp.getStartupOutput(), 'Mode:DOCKER\nVersion:TEST-1.2.3\nFrontend Location:../app\n')


