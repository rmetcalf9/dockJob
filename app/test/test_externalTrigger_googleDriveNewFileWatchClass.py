from TestHelperSuperClass import testHelperAPIClient, env
import json
from commonJSONStrings import data_simpleJobCreateParams, data_simpleJobCreateExpRes, data_simpleManualJobCreateParams
import pytest
from appObj import appObj
import copy
from TestHelperWithAPIOperations import TestHelperWithAPIOperationsClass
from appObj import appObj
from APIClients import GoogleNotFoundException
from unittest.mock import patch

class helper(TestHelperWithAPIOperationsClass):
    def setup(self):
        result = self.testClient.post('/api/jobs/', data=json.dumps(data_simpleJobCreateParams), content_type='application/json')
        self.assertResponseCodeEqual(result, 200)
        return {
            "setupJob": json.loads(result.text)
        }

@pytest.mark.externalTriggerSystemTest
class test_externalTrigger_googleDriveNewFileWatchClass(helper):

    def test_activateapionjob_google_client_not_activated(self):
        setup = self.setup()
        appObj.DOCKJOB_APICLIENT_GOOGLE_CLIENT_SECRET_FILE = "notactive"

        triggerOptions={
            "refresh_token": "dummy_google_refresh_token",
            "folder_path": "/a/b/validfolder"
        }

        activate_response = self.activateTriggerOnJob(
            jobGuid=setup["setupJob"]["guid"],
            triggerType="googleDriveNewFileWatchClass",
            triggerOptions=triggerOptions,
            check_and_parse_response=False
        )
        self.assertEqual(activate_response.status_code, 400)
        response_json = json.loads(activate_response.text)
        self.assertEqual(response_json["result"], "Fail")
        self.assertEqual(response_json["message"], "Google client not activated")

    def test_activateapionjob_missing_refreshtoken(self):
        setup = self.setup()

        triggerOptions={
            "folder_path": "/a/b/validfolder"
        }

        activate_response = self.activateTriggerOnJob(
            jobGuid=setup["setupJob"]["guid"],
            triggerType="googleDriveNewFileWatchClass",
            triggerOptions=triggerOptions,
            check_and_parse_response=False
        )
        self.assertEqual(activate_response.status_code, 400)
        response_json = json.loads(activate_response.text)
        self.assertEqual(response_json["result"], "Fail")
        self.assertEqual(response_json["message"], "Missing refresh_token")

    def test_activateapionjob_missing_folder(self):
        setup = self.setup()

        triggerOptions={
            "refresh_token": "dummy_google_refresh_token"
        }

        activate_response = self.activateTriggerOnJob(
            jobGuid=setup["setupJob"]["guid"],
            triggerType="googleDriveNewFileWatchClass",
            triggerOptions=triggerOptions,
            check_and_parse_response=False
        )
        self.assertEqual(activate_response.status_code, 400)
        response_json = json.loads(activate_response.text)
        self.assertEqual(response_json["result"], "Fail")
        self.assertEqual(response_json["message"], "Missing folder")

    def test_activateapionjob_test_invalid_folder(self):
        setup = self.setup()

        triggerOptions={
            "refresh_token": "dummy_google_refresh_token_valid",
            "folder_path": "/a/b/invalidfolder"
        }
        with patch('APIClients.DriveApiHelpers.find_folder_from_path', side_effect=GoogleNotFoundException('mocked error')):
            activate_response = self.activateTriggerOnJob(
                jobGuid=setup["setupJob"]["guid"],
                triggerType="googleDriveNewFileWatchClass",
                triggerOptions=triggerOptions,
                check_and_parse_response=False
            )
        self.assertEqual(activate_response.status_code, 400)
        response_json = json.loads(activate_response.text)
        self.assertEqual(response_json["result"], "Fail")
        self.assertEqual(response_json["message"], "Invalid Folder")

    def test_activateapionjob_test_valid(self):
        setup = self.setup()

        triggerOptions={
            "refresh_token": "dummy_google_refresh_token_valid",
            "folder_path": "/a/b/invalidfolder"
        }
        dummy_file = { "id": "aaa" }
        with patch('APIClients.DriveApiHelpers.find_folder_from_path', result=dummy_file):
            activate_response = self.activateTriggerOnJob(
                jobGuid=setup["setupJob"]["guid"],
                triggerType="googleDriveNewFileWatchClass",
                triggerOptions=triggerOptions,
                check_and_parse_response=False
            )
        self.assertEqual(activate_response.status_code, 201)
        #response_json = json.loads(activate_response.text)
        #print("response_json", response_json)


    #New file list mock response:
    #  [{'mimeType': 'application/pdf', 'parents': ['1LhOLAK3AC3XYGm3mr2MpZ1uM0BJPcDwJ'], 'id': '1TjGK6F532IpG881Fu-f5JbYYvZOhoiWM', 'name': 'Scanned_20231118-2054.pdf'}]