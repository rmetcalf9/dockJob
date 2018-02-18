import unittest
from FlaskRestSubclass import FlaskRestSubclass
from GlobalParamaters import GlobalParamaters
from urllib.parse import urlparse

class mockGlobalPamaters():
  apidocsurl = "https://cat-sdts.metcarob-home.com/dockjobapidocs/"

  def getSanitizedPath(self, url):
    a = urlparse(url).path.strip()
    if (a[-1:] == '/'):
      a = a[:-1]
    return a
  def getAPIDOCSPath(self):
    return self.getSanitizedPath(self.apidocsurl)

 
class test_FlaskRestSubclass(unittest.TestCase):
 
    def test_replacementsSingle(self):
      GlobalParamaters.set(mockGlobalPamaters())
      api = FlaskRestSubclass(None, version='1.0', title='TodoMVC API',
        description='A simple TodoMVC API', doc='/'
      )
      initial = "\"http://dockjob/api/swagger.json\""
      expected = "\"https://cat-sdts.metcarob-home.com/dockjobapidocs/swagger.json\""
      res = api.reaplcements(initial)
      self.assertEqual(expected, res)

    def test_replacementsSingleHTTPS(self):
      GlobalParamaters.set(mockGlobalPamaters())
      api = FlaskRestSubclass(None, version='1.0', title='TodoMVC API',
        description='A simple TodoMVC API', doc='/'
      )
      initial = "\"https://dockjob/api/swagger.json\""
      expected = "\"https://cat-sdts.metcarob-home.com/dockjobapidocs/swagger.json\""
      res = api.reaplcements(initial)
      self.assertEqual(expected, res)

    def test_replacementsSingleHTTPSWithPort(self):
      GlobalParamaters.set(mockGlobalPamaters())
      api = FlaskRestSubclass(None, version='1.0', title='TodoMVC API',
        description='A simple TodoMVC API', doc='/'
      )
      initial = "\"https://dockjob:123/api/swagger.json\""
      expected = "\"https://cat-sdts.metcarob-home.com/dockjobapidocs/swagger.json\""
      res = api.reaplcements(initial)
      self.assertEqual(expected, res)

    def test_replacementsShort(self):
      GlobalParamaters.set(mockGlobalPamaters())
      api = FlaskRestSubclass(None, version='1.0', title='TodoMVC API',
        description='A simple TodoMVC API', doc='/'
      )
      initial = "sadsad asdds \"http://urlnottoreplace.com\" - \"http://dockjob/api/swagger.json\""
      expected = "sadsad asdds \"http://urlnottoreplace.com\" - \"https://cat-sdts.metcarob-home.com/dockjobapidocs/swagger.json\""
      res = api.reaplcements(initial)
      self.assertEqual(expected, res)


    def test_replacements(self):
      GlobalParamaters.set(mockGlobalPamaters())
      api = FlaskRestSubclass(None, version='1.0', title='TodoMVC API',
        description='A simple TodoMVC API', doc='/'
      )
      initial = "sadsad asdds \"http://urlnottoreplace.com\"\n\"http://dockjob/api/swagger.json\"\nsdddsds\n\"https://dockjob/api/swagger.json\"\nadsd\n\"http://dockjob:333/api/swagger.json\"\nssdd\n\"https://dock-job:333/api/swagger.json\"\nsadds\n\"http://asdsasd:33/test.xmxl\"\nsdd\n\"https://dock.job:333/api/swagger.json\"\nsadds"
      expected = "sadsad asdds \"http://urlnottoreplace.com\"\n\"https://cat-sdts.metcarob-home.com/dockjobapidocs/swagger.json\"\nsdddsds\n\"https://cat-sdts.metcarob-home.com/dockjobapidocs/swagger.json\"\nadsd\n\"https://cat-sdts.metcarob-home.com/dockjobapidocs/swagger.json\"\nssdd\n\"https://cat-sdts.metcarob-home.com/dockjobapidocs/swagger.json\"\nsadds\n\"http://asdsasd:33/test.xmxl\"\nsdd\n\"https://cat-sdts.metcarob-home.com/dockjobapidocs/swagger.json\"\nsadds"
      res = api.reaplcements(initial)
      self.assertEqual(expected, res)

    def test_srcReplacementSRC(self):
      GlobalParamaters.set(mockGlobalPamaters())
      api = FlaskRestSubclass(None, version='1.0', title='TodoMVC API',
        description='A simple TodoMVC API', doc='/'
      )
      initial = "<script src=\"/apidocs/swaggerui/bower/swagger-ui/dist/lib/jquery.wiggle.min.js\" type=\"text/javascript\"></script>\n<script src=\"/apidocs/swaggerui/bower/swagger-ui/dist/lib/jquery.ba-bbq.min.js\" type=\"text/javascript\"></script>"
      expected = "<script src=\"/dockjobapidocs/swaggerui/bower/swagger-ui/dist/lib/jquery.wiggle.min.js\" type=\"text/javascript\"></script>\n<script src=\"/dockjobapidocs/swaggerui/bower/swagger-ui/dist/lib/jquery.ba-bbq.min.js\" type=\"text/javascript\"></script>"
      res = api.reaplcements(initial)
      self.assertEqual(expected, res)


    def test_srcReplacementMixed(self):
      GlobalParamaters.set(mockGlobalPamaters())
      api = FlaskRestSubclass(None, version='1.0', title='TodoMVC API',
        description='A simple TodoMVC API', doc='/'
      )
      api.internalAPIPath='/apidocs' #Test against a different internal directory
      initial = "sadsad asdds \"http://urlnottoreplace.com\"\n\"http://dockjob/apidocs/swagger.json\"\nsdddsds\n\"https://dockjob/apidocs/swagger.json\"\nadsd\n\"http://dockjob:333/apidocs/swagger.json\"\nssdd\n\"https://dock-job:333/apidocs/swagger.json\"\nsadds\n\"http://asdsasd:33/test.xmxl\"\nsdd\n\"https://dock.job:333/apidocs/swagger.json\"\nsadds"
      expected = "sadsad asdds \"http://urlnottoreplace.com\"\n\"https://cat-sdts.metcarob-home.com/dockjobapidocs/swagger.json\"\nsdddsds\n\"https://cat-sdts.metcarob-home.com/dockjobapidocs/swagger.json\"\nadsd\n\"https://cat-sdts.metcarob-home.com/dockjobapidocs/swagger.json\"\nssdd\n\"https://cat-sdts.metcarob-home.com/dockjobapidocs/swagger.json\"\nsadds\n\"http://asdsasd:33/test.xmxl\"\nsdd\n\"https://cat-sdts.metcarob-home.com/dockjobapidocs/swagger.json\"\nsadds"
      initial2 = "<script src=\"/apidocs/swaggerui/bower/swagger-ui/dist/lib/jquery.wiggle.min.js\" type=\"text/javascript\"></script>\n<script src=\"/apidocs/swaggerui/bower/swagger-ui/dist/lib/jquery.ba-bbq.min.js\" type=\"text/javascript\"></script>"
      expected2 = "<script src=\"/dockjobapidocs/swaggerui/bower/swagger-ui/dist/lib/jquery.wiggle.min.js\" type=\"text/javascript\"></script>\n<script src=\"/dockjobapidocs/swaggerui/bower/swagger-ui/dist/lib/jquery.ba-bbq.min.js\" type=\"text/javascript\"></script>"
      res = api.reaplcements(initial + initial2)
      self.assertEqual(expected + expected2, res)

    def test_swaggerJSONReplaceFromContainer(self):
      mockGP = mockGlobalPamaters()
      GlobalParamaters.set(mockGP)
      api = FlaskRestSubclass(None, version='1.0', title='TodoMVC API',
        description='A simple TodoMVC API', doc='/'
      )
      initial = "            window.swaggerUi = new SwaggerUi({                url: \"http://dockjob/api/swagger.json\",                validatorUrl: \"\" || null,"
      expected = "            window.swaggerUi = new SwaggerUi({                url: \"https://cat-sdts.metcarob-home.com/dockjobapidocs/swagger.json\",                validatorUrl: \"\" || null,"
      res = api.reaplcements(initial)
      self.assertEqual(expected, res)



