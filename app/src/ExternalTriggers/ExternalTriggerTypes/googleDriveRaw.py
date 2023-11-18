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
        return True

    # Return value (updateJobNeeded, typeprivatevars, typepublicvars)
    def fireTrigger(self, submitJobFunction, jobData, urlid, request_headers, request_data, rawurlpasscode, rawnonurlpasscode):
        # Not public and private VARS are in jobData
        ## print("typeprivatevars", jobData.__dict__["PrivateExternalTrigger"]["typeprivatevars"])
        ## print("typepublicvars", jobData.__dict__["PrivateExternalTrigger"]["typepublicvars"])

        dataForStdin = {
            "headers": {**request_headers},
            "request_data": request_data.decode("utf-8")
        }

        submitJobFunction(
            stdinData=json.dumps(dataForStdin).encode("utf-8"),
            executionName="Triggered by " + jobData.__dict__["PrivateExternalTrigger"]["type"]
        )

        return (
            False, # updateJobNeeded
            None, # typeprivatevars
            None # typepublicvars
        )
