import unittest
from FlaskRestSubclass import FlaskRestSubclass
from urllib.parse import urlparse


#  def setExtraParams(apidocsurl, APIDOCSPath, overrideAPIDOCSPath, APIPath):


def getSanitizedPath(url):
  a = urlparse(url).path.strip()
  if (a[-1:] == '/'):
    a = a[:-1]
  return a

apidocsurl = "https://cat-sdts.metcarob-home.com/dockjobapidocs/"
APIDOCSPath = getSanitizedPath(apidocsurl)
overrideAPIDOCSPath = None
APIPath = None



class test_FlaskRestSubclass(unittest.TestCase):
 
    def test_replacementsSingle(self):
      api = FlaskRestSubclass(None, version='1.0', title='TodoMVC API',
        description='A simple TodoMVC API', doc='/'
      )
      api.setExtraParams(apidocsurl, APIDOCSPath, overrideAPIDOCSPath, APIPath)
      initial = "\"http://dockjob/api/swagger.json\""
      expected = "\"https://cat-sdts.metcarob-home.com/dockjobapidocs/swagger.json\""
      res = api.reaplcements(initial)
      self.assertEqual(expected, res)

    def test_replacementsSingleHTTPS(self):
      api = FlaskRestSubclass(None, version='1.0', title='TodoMVC API',
        description='A simple TodoMVC API', doc='/'
      )
      api.setExtraParams(apidocsurl, APIDOCSPath, overrideAPIDOCSPath, APIPath)
      initial = "\"https://dockjob/api/swagger.json\""
      expected = "\"https://cat-sdts.metcarob-home.com/dockjobapidocs/swagger.json\""
      res = api.reaplcements(initial)
      self.assertEqual(expected, res)

    def test_replacementsSingleHTTPSWithPort(self):
      api = FlaskRestSubclass(None, version='1.0', title='TodoMVC API',
        description='A simple TodoMVC API', doc='/'
      )
      api.setExtraParams(apidocsurl, APIDOCSPath, overrideAPIDOCSPath, APIPath)
      initial = "\"https://dockjob:123/api/swagger.json\""
      expected = "\"https://cat-sdts.metcarob-home.com/dockjobapidocs/swagger.json\""
      res = api.reaplcements(initial)
      self.assertEqual(expected, res)

    def test_replacementsShort(self):
      api = FlaskRestSubclass(None, version='1.0', title='TodoMVC API',
        description='A simple TodoMVC API', doc='/'
      )
      api.setExtraParams(apidocsurl, APIDOCSPath, overrideAPIDOCSPath, APIPath)
      initial = "sadsad asdds \"http://urlnottoreplace.com\" - \"http://dockjob/api/swagger.json\""
      expected = "sadsad asdds \"http://urlnottoreplace.com\" - \"https://cat-sdts.metcarob-home.com/dockjobapidocs/swagger.json\""
      res = api.reaplcements(initial)
      self.assertEqual(expected, res)


    def test_replacements(self):
      api = FlaskRestSubclass(None, version='1.0', title='TodoMVC API',
        description='A simple TodoMVC API', doc='/'
      )
      api.setExtraParams(apidocsurl, APIDOCSPath, overrideAPIDOCSPath, APIPath)
      initial = "sadsad asdds \"http://urlnottoreplace.com\"\n\"http://dockjob/api/swagger.json\"\nsdddsds\n\"https://dockjob/api/swagger.json\"\nadsd\n\"http://dockjob:333/api/swagger.json\"\nssdd\n\"https://dock-job:333/api/swagger.json\"\nsadds\n\"http://asdsasd:33/test.xmxl\"\nsdd\n\"https://dock.job:333/api/swagger.json\"\nsadds"
      expected = "sadsad asdds \"http://urlnottoreplace.com\"\n\"https://cat-sdts.metcarob-home.com/dockjobapidocs/swagger.json\"\nsdddsds\n\"https://cat-sdts.metcarob-home.com/dockjobapidocs/swagger.json\"\nadsd\n\"https://cat-sdts.metcarob-home.com/dockjobapidocs/swagger.json\"\nssdd\n\"https://cat-sdts.metcarob-home.com/dockjobapidocs/swagger.json\"\nsadds\n\"http://asdsasd:33/test.xmxl\"\nsdd\n\"https://cat-sdts.metcarob-home.com/dockjobapidocs/swagger.json\"\nsadds"
      res = api.reaplcements(initial)
      self.assertEqual(expected, res)

    def test_srcReplacementSRC(self):
      api = FlaskRestSubclass(None, version='1.0', title='TodoMVC API',
        description='A simple TodoMVC API', doc='/'
      )
      api.setExtraParams(apidocsurl, APIDOCSPath, overrideAPIDOCSPath, APIPath)
      initial = "<script src=\"/apidocs/swaggerui/bower/swagger-ui/dist/lib/jquery.wiggle.min.js\" type=\"text/javascript\"></script>\n<script src=\"/apidocs/swaggerui/bower/swagger-ui/dist/lib/jquery.ba-bbq.min.js\" type=\"text/javascript\"></script>"
      expected = "<script src=\"/dockjobapidocs/swaggerui/bower/swagger-ui/dist/lib/jquery.wiggle.min.js\" type=\"text/javascript\"></script>\n<script src=\"/dockjobapidocs/swaggerui/bower/swagger-ui/dist/lib/jquery.ba-bbq.min.js\" type=\"text/javascript\"></script>"
      res = api.reaplcements(initial)
      self.assertEqual(expected, res)


    def test_srcReplacementMixed(self):
      api = FlaskRestSubclass(None, version='1.0', title='TodoMVC API',
        description='A simple TodoMVC API', doc='/'
      )
      api.setExtraParams(apidocsurl, APIDOCSPath, overrideAPIDOCSPath, APIPath)
      api.internalAPIPath='/apidocs' #Test against a different internal directory
      initial = "sadsad asdds \"http://urlnottoreplace.com\"\n\"http://dockjob/apidocs/swagger.json\"\nsdddsds\n\"https://dockjob/apidocs/swagger.json\"\nadsd\n\"http://dockjob:333/apidocs/swagger.json\"\nssdd\n\"https://dock-job:333/apidocs/swagger.json\"\nsadds\n\"http://asdsasd:33/test.xmxl\"\nsdd\n\"https://dock.job:333/apidocs/swagger.json\"\nsadds"
      expected = "sadsad asdds \"http://urlnottoreplace.com\"\n\"https://cat-sdts.metcarob-home.com/dockjobapidocs/swagger.json\"\nsdddsds\n\"https://cat-sdts.metcarob-home.com/dockjobapidocs/swagger.json\"\nadsd\n\"https://cat-sdts.metcarob-home.com/dockjobapidocs/swagger.json\"\nssdd\n\"https://cat-sdts.metcarob-home.com/dockjobapidocs/swagger.json\"\nsadds\n\"http://asdsasd:33/test.xmxl\"\nsdd\n\"https://cat-sdts.metcarob-home.com/dockjobapidocs/swagger.json\"\nsadds"
      initial2 = "<script src=\"/apidocs/swaggerui/bower/swagger-ui/dist/lib/jquery.wiggle.min.js\" type=\"text/javascript\"></script>\n<script src=\"/apidocs/swaggerui/bower/swagger-ui/dist/lib/jquery.ba-bbq.min.js\" type=\"text/javascript\"></script>"
      expected2 = "<script src=\"/dockjobapidocs/swaggerui/bower/swagger-ui/dist/lib/jquery.wiggle.min.js\" type=\"text/javascript\"></script>\n<script src=\"/dockjobapidocs/swaggerui/bower/swagger-ui/dist/lib/jquery.ba-bbq.min.js\" type=\"text/javascript\"></script>"
      res = api.reaplcements(initial + initial2)
      self.assertEqual(expected + expected2, res)

    def test_swaggerJSONReplaceFromContainer(self):
      api = FlaskRestSubclass(None, version='1.0', title='TodoMVC API',
        description='A simple TodoMVC API', doc='/'
      )
      api.setExtraParams(apidocsurl, APIDOCSPath, overrideAPIDOCSPath, APIPath)
      initial = "            window.swaggerUi = new SwaggerUi({                url: \"http://dockjob/api/swagger.json\",                validatorUrl: \"\" || null,"
      expected = "            window.swaggerUi = new SwaggerUi({                url: \"https://cat-sdts.metcarob-home.com/dockjobapidocs/swagger.json\",                validatorUrl: \"\" || null,"
      res = api.reaplcements(initial)
      self.assertEqual(expected, res)

    def test_cssJSONReplaceFromContainer(self):
      api = FlaskRestSubclass(None, version='1.0', title='TodoMVC API',
        description='A simple TodoMVC API', doc='/'
      )
      api.setExtraParams(apidocsurl, APIDOCSPath, overrideAPIDOCSPath, APIPath)
      initial = "<link media=\"screen\" rel=\"stylesheet\" type=\"text/css\"    href=\"/apidocs/swaggerui/bower/swagger-ui/dist/css/reset.css\" />\n<link media=\"screen\" rel=\"stylesheet\" type=\"text/css\"    href=\"/apidocs/swaggerui/bower/swagger-ui/dist/css/screen.css\" />"
      expected = "<link media=\"screen\" rel=\"stylesheet\" type=\"text/css\"    href=\"/dockjobapidocs/swaggerui/bower/swagger-ui/dist/css/reset.css\" />\n<link media=\"screen\" rel=\"stylesheet\" type=\"text/css\"    href=\"/dockjobapidocs/swaggerui/bower/swagger-ui/dist/css/screen.css\" />"
      res = api.reaplcements(initial)
      self.assertEqual(expected, res)


