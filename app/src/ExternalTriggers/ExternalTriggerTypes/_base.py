
class externalTriggerBaseClass():
    def getStaticServerInfoData(self):
        return {}

    def getEncodedJobGuidFromMessage(self, urlid, request_headers, request_data):
        return None

    def requestMatches(self, jobData, urlid, request_headers, request_data, rawurlpasscode, rawnonurlpasscode):
        return False

    def activate(self, jobguid, triggerType, jobObj, triggerOptions, salt, urlpasscode, nonurlpasscode):
        # Only ever called when the job has no trigger activated
        # by default nothing to do
        return (None, {}, {})

    def deactivate(self, jobguid, privateTriggerData):
        return
