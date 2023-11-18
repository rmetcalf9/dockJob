from ._base import externalTriggerBaseClass
import json

class googleDriveRawClass(externalTriggerBaseClass):
    def getEncodedJobGuidFromMessage(self, urlid, request_headers, request_data):
        if "X-Goog-Channel-Token" not in request_headers:
            return None
        return request_headers["X-Goog-Channel-Token"]

    def requestMatches(self, jobData, urlid, request_headers, request_data, rawurlpasscode, rawnonurlpasscode):
        PrivateExternalTrigger = jobData.__dict__["PrivateExternalTrigger"]
        if not PrivateExternalTrigger["triggerActive"]:
            return False

        if urlid != rawurlpasscode:
            return False

        if request_headers["X-Goog-Channel-ID"] != rawnonurlpasscode:
            return False

        # TODO I need to add all my data items to the Job object

        return True

    def getStdinData(self, jobData, urlid, request_headers, request_data, rawurlpasscode, rawnonurlpasscode):
        dataForStdin = {
            "headers": {**request_headers},
            "request_data": request_data.decode("utf-8")
        }
        return json.dumps(dataForStdin).encode("utf-8")
