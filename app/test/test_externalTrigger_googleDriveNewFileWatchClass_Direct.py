from ExternalTriggers import getAllTriggerTypeInstances
import pytest
import pytz
import datetime
import unittest
from unittest.mock import patch

class MockExternalTriggerManager():
    class appObj():
        DOCKJOB_APICLIENT_GOOGLE_CLIENT_SECRET_FILE="sf"
        APIAPP_TRIGGERAPIURL="d"
    appObj = appObj()

    def encodeJobGuid(self, jobOBj):
        return "TT"

class MockGoogleClient():
    pass

class MockJobObjNoExpiry():
    PrivateExternalTrigger = {
        "typeprivatevars": {},
        "typepublicvars": {}
    }

class MockJobObj():
    guid = "123"
    PrivateExternalTrigger = {
        "typeprivatevars": {
            "refresh_token": "dummy_refresh_token",
            "current_watch_resource_id": "dumm",
            "folder_id": "dd"
        },
        "typepublicvars": {}
    }
    def __init__(self, current_watch_expiry):
        self.PrivateExternalTrigger["typepublicvars"]["current_watch_expiry"] = current_watch_expiry

def getJobPasscodes(jobObj):
    return ("rawurlpasscode", "rawnonurlpasscode")

@pytest.mark.externalTriggerSystemTest
class test_googledrivewatchnew_direct(unittest.TestCase):
    def test_loopiteration_no_expiry_field(self):
        testStartTime = pytz.timezone('UTC').localize(datetime.datetime(2018,1,1,13,46,0,0))

        mockExternalTriggerManager = MockExternalTriggerManager()
        mockJobObj = MockJobObjNoExpiry()

        triggers = getAllTriggerTypeInstances(mockExternalTriggerManager)
        trigger = triggers["googleDriveNewFileWatchClass"]

        self.assertEqual(
            trigger.loopIterationForJob(mockJobObj, testStartTime, getJobPasscodes=None),
            (False, None, None, None, None)
        )

    def test_loopiteration_not_expired(self):
        testStartTime = pytz.timezone('UTC').localize(datetime.datetime(2018,1,1,13,46,0,0))

        mockExternalTriggerManager = MockExternalTriggerManager()
        mockJobObj = MockJobObj(
            current_watch_expiry=(testStartTime + datetime.timedelta(days=7)).timestamp() * 1000
        )

        triggers = getAllTriggerTypeInstances(mockExternalTriggerManager)
        trigger = triggers["googleDriveNewFileWatchClass"]


        self.assertEqual(
            trigger.loopIterationForJob(mockJobObj, testStartTime, getJobPasscodes=None),
            (False, None, None, None, None)
        )

    def test_loopiteration_has_expired(self):
        testStartTime = pytz.timezone('UTC').localize(datetime.datetime(2018,1,1,13,46,0,0))

        mockExternalTriggerManager = MockExternalTriggerManager()
        mockJobObj = MockJobObj(
            current_watch_expiry=(testStartTime - datetime.timedelta(days=7)).timestamp() * 1000
        )
        def mockGoogleClientInit(a, b):
            return None

        triggers = getAllTriggerTypeInstances(mockExternalTriggerManager)
        trigger = triggers["googleDriveNewFileWatchClass"]

        newWatchExpiry="1234"

        with patch('APIClients.GoogleClient.__init__', mockGoogleClientInit):
            def clear_watch_on_files(a, channel_id,resource_id):
                return None
            with patch('APIClients.DriveApiHelpers.clear_watch_on_files', clear_watch_on_files):
                def dummy_setup_watch_on_files(a, file_id, trigger_url, channel_id, token):
                    return {
                        "resourceId": "dummyChannelresourceid",
                        "expiration": newWatchExpiry
                    }

                with patch('APIClients.DriveApiHelpers.setup_watch_on_files', dummy_setup_watch_on_files):
                    def nw():
                        return "newuuid"
                    with patch('uuid.uuid4', nw):
                        (updateJobNeeded, typeprivatevars, typepublicvars, newrawurlpasscode, newrawnonurlpasscode) = trigger.loopIterationForJob(mockJobObj, testStartTime, getJobPasscodes=getJobPasscodes)
                        self.assertEqual(updateJobNeeded, True)
                        self.assertEqual(typeprivatevars, {
                            "current_watch_resource_id": mockJobObj.PrivateExternalTrigger["typeprivatevars"]["current_watch_resource_id"],
                            "folder_id": mockJobObj.PrivateExternalTrigger["typeprivatevars"]["folder_id"],
                            "refresh_token": mockJobObj.PrivateExternalTrigger["typeprivatevars"]["refresh_token"]
                        })
                        self.assertEqual(typepublicvars, {'current_watch_expiry': newWatchExpiry})
                        self.assertEqual(newrawurlpasscode, nw())
                        self.assertEqual(newrawnonurlpasscode, nw())

