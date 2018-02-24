from TestHelperSuperClass import testHelperAPIClient

import json
from utils import from_iso8601
import api


class test_jobsData(testHelperAPIClient):
  def test_JobCreate(self):
    params = {
      "name": "TestJob",
      "repetitionInterval": "HOURLY:03",
      "command": "ls",
      "enabled": True
    }
    expRes = {
      "guid": 'IGNORE', 
      "name": params['name'], 
      "command": params['command'], 
      "enabled": params['enabled'], 
      "repetitionInterval": params['repetitionInterval'], 
      "creationDate": "IGNORE", 
      "lastUpdateDate": "IGNORE",
      "lastRunDate": None,
    }
    result = self.testClient.post('/api/jobs/', data=json.dumps(params), content_type='application/json')
    self.assertEqual(result.status_code, 200)
    resultJSON = json.loads(result.get_data(as_text=True))
    self.assertTrue(len(resultJSON['guid']) == 36, msg='Invalid GUID - must be 36 chars')
    self.assertTrue(resultJSON['creationDate'] == resultJSON['lastUpdateDate'], msg='Creation date dosen''t match last update')
    tim = from_iso8601(resultJSON['creationDate'])
    self.assertTimeCloseToCurrent(tim)
    resultJSON['guid'] = expRes['guid']
    resultJSON['creationDate'] = expRes['creationDate']
    resultJSON['lastUpdateDate'] = expRes['lastUpdateDate']
    self.assertJSONStringsEqual(resultJSON, expRes);
