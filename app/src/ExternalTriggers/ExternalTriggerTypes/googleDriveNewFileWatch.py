from ._base import externalTriggerBaseClass
from APIClients import GoogleClient, GoogleNotFoundException, GoogleUnauthorizedExceptoin
import json
import uuid

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
            "file_id_list": file_id_list,
            "current_watch_resource_id": watch_response["resourceId"]
        }
        typepublicvars = {
            "folder_path": triggerOptions["folder_path"],
            "current_watch_expiry": watch_response["expiration"]
        }

        return (None, typeprivatevars, typepublicvars)

    def deactivate(self, jobObj, rawurlpasscode, rawnonurlpasscode):
        typeprivatevars = jobObj.PrivateExternalTrigger["typeprivatevars"]
        typepublicvars = jobObj.PrivateExternalTrigger["typepublicvars"]
        google_client = GoogleClient(self.externalTriggerManager.appObj.DOCKJOB_APICLIENT_GOOGLE_CLIENT_SECRET_FILE)
        google_client.setup_auth(
            refresh_token=typeprivatevars["refresh_token"]
        )
        try:
            deactivate_response = google_client.drive().clear_watch_on_files(
                channel_id=rawnonurlpasscode,
                resource_id= typeprivatevars["current_watch_resource_id"]
            )
        except:
            print("WARNING - googleDriveNewFileWatch failed to remove watch. Igniring as it will timeout anyway")
        return

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
        typeprivatevars = jobData.PrivateExternalTrigger["typeprivatevars"]
        typepublicvars = jobData.PrivateExternalTrigger["typepublicvars"]

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

    # Return value (updateJobNeeded, typeprivatevars, typepublicvars)
    def loopIterationForJob(self, jobObj, curTime, getJobPasscodes):
        typeprivatevars = jobObj.PrivateExternalTrigger["typeprivatevars"]
        typepublicvars = jobObj.PrivateExternalTrigger["typepublicvars"]
        if "current_watch_expiry" not in typepublicvars:
            return (False, None, None, None, None)
        if "suspended" in typepublicvars:
            return (False, None, None, None, None)
        if int(typepublicvars["current_watch_expiry"]) >= (curTime.timestamp()*1000):
            return (False, None, None, None, None)

        # Google watch has expired
        #  there is no way to renew it
        #  we must destory and recrate it
        #  but we need to use different id as new and old watches may exist at same time
        #  we don't need to worry about missing or duplicating messages as we are just using notification to
        #  trigger our alogrythm and we rmemeber file id's ourselves

        (rawurlpasscode, rawnonurlpasscode) = getJobPasscodes(jobObj)

        google_client = GoogleClient(self.externalTriggerManager.appObj.DOCKJOB_APICLIENT_GOOGLE_CLIENT_SECRET_FILE)
        google_client.setup_auth(
            refresh_token=typeprivatevars["refresh_token"]
        )
        #deactivate Not strictly nessecary - watch has expired anyway
        try:
            deactivate_response = google_client.drive().clear_watch_on_files(
                channel_id=rawnonurlpasscode,
                resource_id=typeprivatevars["current_watch_resource_id"]
            )
        except:
            print("WARNING - googleDriveNewFileWatch expiration failed to remove watch. Ignoring as it will timeout anyway (or it expired)")

        newrawurlpasscode = str(uuid.uuid4())
        newrawnonurlpasscode = str(uuid.uuid4())

        watch_response = None
        try:
            watch_response = google_client.drive().setup_watch_on_files(
                file_id=typeprivatevars["folder_id"],
                trigger_url=self.externalTriggerManager.appObj.APIAPP_TRIGGERAPIURL + "/trigger/" + newrawurlpasscode,
                channel_id=newrawnonurlpasscode,
                token=self.externalTriggerManager.encodeJobGuid(jobObj.guid)
            )
        except Exception as err:
            print("****")
            print("ERROR - googleDriveNewFileWatch activate watch failed. Ignoring error and continuing thread")
            print("****")
            print(err)  # for the repr
            print(str(err))  # for just the message
            print(err.args)  # the arguments that the exception has been called with.
            print("****")
            typepublicvars["suspended"] = True
            typepublicvars["error"] = str(err)
            return (True, typeprivatevars, typepublicvars, None, None)

        typeprivatevars["refresh_token"] = google_client.get_current_refresh_token()
        typeprivatevars["current_watch_resource_id"] = watch_response["resourceId"]
        typepublicvars["current_watch_expiry"] = watch_response["expiration"]

        return (True, typeprivatevars, typepublicvars, newrawurlpasscode, newrawnonurlpasscode)