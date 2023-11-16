from .ExternalTriggerTypes import getAllTriggerTypeInstances
from .api import register_api
from encryption import getSafePasswordString, decryptPassword, encryptPassword
from flask_restx import fields

saltForJobIdPasswordEncryption="JDJiJDEyJFRGQmZ1RzhjY3IzVTVxTzVTeERXbnU="

class ExternalTriggerManager():
    safePasswordString = None
    appObj = None

    TriggerTypes = None
    def __init__(self, DOCKJOB_EXTERNAL_TRIGGER_SYS_PASSWORD, appObj):
        self.safePasswordString = getSafePasswordString(DOCKJOB_EXTERNAL_TRIGGER_SYS_PASSWORD)
        self.appObj = appObj
        self.TriggerTypes = getAllTriggerTypeInstances()

    def getStaticServerInfoData(self):
        types = {}
        for type in self.TriggerTypes:
            types[type] = self.TriggerTypes[type].getStaticServerInfoData()
        return {
            "types": types
        }

    def encodeJobGuid(self, job_guid):
        return encryptPassword(self.appObj.bcrypt, job_guid, saltForJobIdPasswordEncryption, self.safePasswordString)
    def decodeJobGuid(self, cypherText):
        #must use hardcoded salt as cannot use salts on the job as we don't know which job yet
        try:
            return decryptPassword(self.appObj.bcrypt, cypherText, saltForJobIdPasswordEncryption, self.safePasswordString)
        except:
            return None

    # 406 means message was received but there are no configured types to process
    def processTrigger(self, urlid, request_headers, request_data):
        possible_jobs_that_could_match = {}
        for type in self.TriggerTypes:
            jobGuid = self.decodeJobGuid(self.TriggerTypes[type].getEncodedJobGuidFromMessage(urlid, request_headers, request_data))
            if jobGuid is not None:
                if jobGuid not in possible_jobs_that_could_match.keys():
                    possible_jobs_that_could_match[jobGuid] = []
                possible_jobs_that_could_match[jobGuid].append(self.TriggerTypes[type])
        if len(possible_jobs_that_could_match) == 0:
            return {"result": "Fail"}, 406
        def dbfn(store_connection):
            return self.processTriggerWithContext(store_connection, possible_jobs_that_could_match, urlid, request_headers, request_data)
        return self.appObj.objectStore.executeInsideTransaction(dbfn)

    def processTriggerWithContext(self, store_connection, possible_jobs_that_could_match, urlid, request_headers, request_data):
        for jobGuid in possible_jobs_that_could_match.keys():
            jobData = self.appObj.appData['jobsData'].getJobRaw(jobGuid)
            if jobData is not None:
                for triggerType in possible_jobs_that_could_match[jobGuid]:
                    if triggerType.requestMatches(jobData, urlid, request_headers, request_data):
                        print("DD", jobData, triggerType)
                        return {"result": "Fail"}, 200

        return {"result": "Fail"}, 406


    def getJobModel(self):
        return self.appObj.flastRestPlusAPIObject.model('triggerActive', {
            'triggerActive': fields.Boolean(default=False, description='Is auto triggeing enabled'),
        })

    def getJobDictData(self, jobObj):
        if not jobObj.PrivateExternalTrigger["triggerActive"]:
            return { "triggerActive": False }

        raise Exception("Not implemented")