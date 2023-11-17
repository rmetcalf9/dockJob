# Static server info is provided by the base class. It has no trailing slash
#   normal serverinfo in this app has the slash. It isn't static.

from TestHelperSuperClass import testHelperAPIClient, env
import unittest
import json
from commonJSONStrings import data_simpleJobCreateParams, data_simpleJobCreateExpRes, data_simpleManualJobCreateParams
import pytest

@pytest.mark.serverInfo
class test_static_server_info_api(testHelperAPIClient):

  def test_getStaticServerInfo(self):
      expRes = {
          'Server': {
              'APIAPP_APIDOCSURL': env["APIAPP_APIDOCSURL"],
              'APIAPP_FRONTENDURL': env["APIAPP_FRONTENDURL"],
              'ServerDatetime': "IGNORE",
              'Version': env["APIAPP_VERSION"]
          },
          'Derived': {
              "APIAPP_TRIGGERAPIURL": env["APIAPP_TRIGGERAPIURL"],
              'ExternalTriggers': {
                  'types': {
                      'googleDriveRawClass': {},
                      'googleDriveNewFileWatchClass': {}
                  }
              }
          }
      }
      result = self.testClient.get('/api/serverinfo')
      self.assertEqual(result.status_code, 200)
      resultJSON = json.loads(result.get_data(as_text=True))
      resultJSON['Server']['ServerDatetime'] = 'IGNORE'
      self.assertJSONStringsEqual(resultJSON, expRes)
