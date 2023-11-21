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
from test_externalTrigger_endpoints import example_changes_recource_message, external_trigger_api_prefix

class helper(TestHelperWithAPIOperationsClass):
    def setup(self):
        result = self.testClient.post('/api/jobs/', data=json.dumps(data_simpleJobCreateParams), content_type='application/json')
        self.assertResponseCodeEqual(result, 200)
        return {
            "setupJob": json.loads(result.text)
        }

    def triggerJob(self, jobguid):
        get_job_response = self.getJob(guid=jobguid)

        ExternalTrigger = get_job_response["ExternalTrigger"]
        rawurlpasscode = ExternalTrigger["urlpasscode"]
        rawnonurlpasscode = ExternalTrigger["nonurlpasscode"]

        encoded_job_guid = appObj.externalTriggerManager.encodeJobGuid(get_job_response["guid"])
        resource_message = copy.deepcopy(example_changes_recource_message)
        resource_message["headers"]["X-Goog-Channel-Token"] = encoded_job_guid
        resource_message["headers"]["X-Goog-Channel-ID"]=rawnonurlpasscode

        result = self.testClient.post(
            external_trigger_api_prefix + '/trigger/' + rawurlpasscode,
            data=resource_message["data"],
            headers=resource_message["headers"]
        )
        self.assertEqual(result.status_code, 200)
        return json.loads(result.text)


@pytest.mark.externalTriggerSystemTest
class test_externalTrigger_googleDriveNewFileWatchClass(helper):

    def test_activateapionjob_google_client_not_activated(self):
        setup = self.setup()
        appObj.DOCKJOB_APICLIENT_GOOGLE_CLIENT_SECRET_FILE = "notactive"

        triggerOptions={
            "access_token": "dummy_google_access_token",
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

    def test_activateapionjob_missing_accesstoken(self):
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
        self.assertEqual(response_json["message"], "Missing access_token")

    def test_activateapionjob_missing_folder(self):
        setup = self.setup()

        triggerOptions={
            "access_token": "dummy_google_access_token"
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
            "access_token": "dummy_google_access_token",
            "folder_path": "/a/b/invalidfolder"
        }
        with patch('APIClients.GoogleClient.refresh_auth', result=None):
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

    def test_activateapionjob_and_trigger_job_no_new_files(self):
        setup = self.setup()

        triggerOptions={
            "access_token": "dummy_google_access_token",
            "folder_path": "/a/b/invalidfolder"
        }
        dummy_file = { "id": "aaa" }
        with patch('APIClients.GoogleClient.refresh_auth', result=None):
            with patch('APIClients.DriveApiHelpers.find_folder_from_path', result=dummy_file):
                def dummy_setup_watch_on_files(a, file_id, trigger_url, channel_id, token):
                    return  {
                        "resourceId": "dummyChannelresourceid",
                        "expiration": "1234"
                    }
                with patch('APIClients.DriveApiHelpers.setup_watch_on_files', dummy_setup_watch_on_files):
                    def a(a, b, c):
                        return ([], [])
                    with patch('APIClients.DriveApiHelpers.get_list_of_new_files', a):
                        activate_response = self.activateTriggerOnJob(
                            jobGuid=setup["setupJob"]["guid"],
                            triggerType="googleDriveNewFileWatchClass",
                            triggerOptions=triggerOptions,
                            check_and_parse_response=False
                        )
        self.assertEqual(activate_response.status_code, 201)

        def a(a, b, c):
            return ([], [])
        with patch('APIClients.DriveApiHelpers.get_list_of_new_files', a):
            trigger_resp = self.triggerJob(
                jobguid = setup["setupJob"]["guid"]
            )
        self.assertEqual(trigger_resp["result"],"Success")


    #New file list mock response:
    #  [{'mimeType': 'application/pdf', 'parents': ['1LhOLAK3AC3XYGm3mr2MpZ1uM0BJPcDwJ'], 'id': '1TjGK6F532IpG881Fu-f5JbYYvZOhoiWM', 'name': 'Scanned_20231118-2054.pdf'}]



