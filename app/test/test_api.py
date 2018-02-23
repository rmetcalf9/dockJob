import unittest
from appObj import appObj
appObj.init()
import api
 
class test_api(unittest.TestCase):

  def setUp(self):
    appObj.init()
  def tearDown(self):
    pass

    def test_getServceInfo(self):
        #calc = Calculator()
        #result = calc.add(2,2)
        #self.assertEqual(6, result)
        pass

