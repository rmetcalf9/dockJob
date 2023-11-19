from ._base import externalTriggerBaseClass
from APIClients import GoogleClient, GoogleNotFoundException, GoogleUnauthorizedExceptoin
import json

class googleDriveNewFileWatchClass(externalTriggerBaseClass):
    #return vars = (failmessage, typeprivatevars, typepublicvars)
    def activate(self, jobguid, triggerType, jobObj, triggerOptions, salt, rawurlpasscode, rawnonurlpasscode):
        if self.externalTriggerManager.appObj.DOCKJOB_APICLIENT_GOOGLE_CLIENT_SECRET_FILE == "notactive":
            return ("Google client not activated", {}, {})

        if "access_token" not in triggerOptions:
            return ("Missing access_token", {}, {})
        if "folder_path" not in triggerOptions:
            return ("Missing folder", {}, {})

        # I thought I needed to exchange access_token for refresh_token - but I think client may do this automatically
        refresh_token = triggerOptions["access_token"]

        google_client = GoogleClient(self.externalTriggerManager.appObj.DOCKJOB_APICLIENT_GOOGLE_CLIENT_SECRET_FILE)
        google_client.setup_auth(
            refresh_token=refresh_token
        )

        try:
            folder_id = google_client.drive().find_folder_from_path(path="/Projects/Property/Business Cards")["id"]
        except GoogleNotFoundException:
            return ("Invalid Folder", {}, {})
        except GoogleUnauthorizedExceptoin:
            return ("Google Unauthorized", {}, {})

        #Set the notification up with google
        watch_response = google_client.drive().setup_watch_on_files(
            file_id=folder_id,
            trigger_url=self.externalTriggerManager.appObj.APIAPP_TRIGGERAPIURL + "/trigger/" + rawurlpasscode,
            channel_id=rawnonurlpasscode,
            token=self.externalTriggerManager.encodeJobGuid(jobObj.__dict__["guid"])
        )

        #Set the folder watcher up and put in initial list of file ids
        (_, file_id_list) = google_client.drive().get_list_of_new_files(folder_id, None)

        typeprivatevars = {
            "folder_id": folder_id,
            "refresh_token": google_client.get_current_refresh_token(),
            "file_id_list": file_id_list
        }
        typepublicvars = {
            "folder_path": triggerOptions["folder_path"]
        }

        return (None, typeprivatevars, typepublicvars)

    def getEncodedJobGuidFromMessage(self, urlid, request_headers, request_data):
        if "X-Goog-Channel-Token" not in request_headers:
            return None
        return request_headers["X-Goog-Channel-Token"]

    def requestMatches(self, jobData, urlid, request_headers, request_data, rawurlpasscode, rawnonurlpasscode):
        if urlid != rawurlpasscode:
            return False
        if request_headers["X-Goog-Channel-ID"] != rawnonurlpasscode:
            return False
        return True

    def fireTrigger(self, submitJobFunction, jobData, urlid, request_headers, request_data, rawurlpasscode, rawnonurlpasscode):
        # Not public and private VARS are in jobData
        ## print("typeprivatevars", jobData.__dict__["PrivateExternalTrigger"]["typeprivatevars"])
        ## print("typepublicvars", jobData.__dict__["PrivateExternalTrigger"]["typepublicvars"])

        typeprivatevars = jobData.__dict__["PrivateExternalTrigger"]["typeprivatevars"]
        typepublicvars = jobData.__dict__["PrivateExternalTrigger"]["typepublicvars"]

        google_client = GoogleClient(self.externalTriggerManager.appObj.DOCKJOB_APICLIENT_GOOGLE_CLIENT_SECRET_FILE)
        google_client.setup_auth(
            refresh_token=typeprivatevars["refresh_token"]
        )

        (new_files, file_id_list) = google_client.drive().get_list_of_new_files(typeprivatevars["folder_id"], typeprivatevars["file_id_list"])

        for new_file in new_files:
            dataForStdin = {
                "event": "newResourceInGoogleDrive",
                "fileInfo": new_file,
                "typepublicvars": typepublicvars,
                "directurl": "https://drive.google.com/uc?export=download&id=" + new_file["id"]
            }
            submitJobFunction(
                stdinData=json.dumps(dataForStdin).encode("utf-8"),
                executionName="Triggered by Triggered by googleDriveNewFileWatchClass - New file " + new_file["name"]
            )

        typeprivatevars["refresh_token"] = google_client.get_current_refresh_token()
        typeprivatevars["file_id_list"] = file_id_list

        return (
            True, # updateJobNeeded
            typeprivatevars, # typeprivatevars
            typepublicvars # typepublicvars
        )
