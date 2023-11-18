from ._base import externalTriggerBaseClass
import json

class googleDriveRawClass(externalTriggerBaseClass):
    def getEncodedJobGuidFromMessage(self, urlid, request_headers, request_data):
        if "X-Goog-Channel-Token" not in request_headers:
            return None
        return request_headers["X-Goog-Channel-Token"]

    def requestMatches(self, jobData, urlid, request_headers, request_data, rawurlpasscode, rawnonurlpasscode):
        if urlid != rawurlpasscode:
            return False

        if request_headers["X-Goog-Channel-ID"] != rawnonurlpasscode:
            return False

        # TODO I need to add all my data items to the Job object

        return True

    # Return value (callNeeded, stdinData, updateJobNeeded, typeprivatevars, typepublicvars)
    def fireTrigger(self, jobData, urlid, request_headers, request_data, rawurlpasscode, rawnonurlpasscode):
        # Not public and private VARS are in jobData
        ## print("typeprivatevars", jobData.__dict__["PrivateExternalTrigger"]["typeprivatevars"])
        ## print("typepublicvars", jobData.__dict__["PrivateExternalTrigger"]["typepublicvars"])

        dataForStdin = {
            "headers": {**request_headers},
            "request_data": request_data.decode("utf-8")
        }
        return (
            True, # callNeeded
            json.dumps(dataForStdin).encode("utf-8"), # stdinData
            False, # updateJobNeeded
            None, # typeprivatevars
            None # typepublicvars
        )
