from TestHelperSuperClass import testHelperAPIClient

from jobsData import t
import json
import pytz
import dateutil.parser

import api


class test_jobsData(testHelperAPIClient):
  def from_iso8601(self, when=None, tz=pytz.timezone("UTC")):
    _when = dateutil.parser.parse(when)
    if not _when.tzinfo:
      _when = tz.localize(_when)
    print(_when.tzinfo)
    if (str(_when.tzinfo) != 'tzutc()'):
      raise Exception('Error - Only conversion of utc times from iso8601 is supported')
    return _when

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
    tim = self.from_iso8601(resultJSON['creationDate'])
    self.assertTimeCloseToCurrent(tim)
    resultJSON['guid'] = expRes['guid']
    resultJSON['creationDate'] = expRes['creationDate']
    resultJSON['lastUpdateDate'] = expRes['lastUpdateDate']
    self.assertJSONStringsEqual(resultJSON, expRes);
