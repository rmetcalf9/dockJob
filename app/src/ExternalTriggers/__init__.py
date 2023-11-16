from .ExternalTriggerTypes import getAllTriggerTypeInstances
from .api import register_api
from .privateApi import register_private_api
from encryption import getSafePasswordString, decryptPassword, encryptPassword, getSafeSaltString
import uuid

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
                PrivateExternalTrigger = jobData.__dict__["PrivateExternalTrigger"]
                if PrivateExternalTrigger["triggerActive"]:
                    print("PrivateExternalTrigger", PrivateExternalTrigger)
                    rawurlpasscode = decryptPassword(self.appObj.bcrypt, PrivateExternalTrigger["urlpasscode"], PrivateExternalTrigger["salt"], self.safePasswordString)
                    rawnonurlpasscode = decryptPassword(self.appObj.bcrypt, PrivateExternalTrigger["nonurlpasscode"], PrivateExternalTrigger["salt"], self.safePasswordString)

                    for triggerType in possible_jobs_that_could_match[jobGuid]:
                        if triggerType.requestMatches(jobData, urlid, request_headers, request_data, rawurlpasscode, rawnonurlpasscode):
                            # TODO Actually launch the job!
                            return {"result": "Success"}, 200

        return {"result": "Fail"}, 406

    def getJobDictData(self, jobObj):
        if not jobObj.PrivateExternalTrigger["triggerActive"]:
            return { "triggerActive": False }

        return {
            "triggerActive": True,
            "type": jobObj.PrivateExternalTrigger["type"],
            "salt": jobObj.PrivateExternalTrigger["salt"],
            "urlpasscode": jobObj.PrivateExternalTrigger["urlpasscode"],
            "nonurlpasscode": jobObj.PrivateExternalTrigger["nonurlpasscode"],
            "typepublicvars": jobObj.PrivateExternalTrigger["typepublicvars"]
        }

    def activateTrigger(self, jobguid, triggerType, triggerOptions):
        if triggerType not in self.TriggerTypes.keys():
            return {"result": "Fail", "message": "Invalid trigger type"}, 400
        def dbfn(store_connection):
            return self.activateTriggerWithStoreConnection(
                store_connection=store_connection,
                jobguid=jobguid,
                triggerType=triggerType,
                triggerTypeObj=self.TriggerTypes[triggerType],
                triggerOptions=triggerOptions
            )
        return self.appObj.objectStore.executeInsideTransaction(dbfn)

    def activateTriggerWithStoreConnection(self, store_connection, jobguid, triggerType, triggerTypeObj, triggerOptions):
        jobObj = self.appObj.appData['jobsData'].getJobRaw(jobguid)
        if jobObj is None:
            return {"result": "Fail", "message": "Job not found"}, 404
        if jobObj.PrivateExternalTrigger["triggerActive"]:
            self.TriggerTypes[triggerType].deactivate(
                jobguid=jobguid,
                privateTriggerData=jobObj.PrivateExternalTrigger
            )

        salt = getSafeSaltString(self.appObj.bcrypt)

        urlpasscode = encryptPassword(self.appObj.bcrypt, str(uuid.uuid4()), salt, self.safePasswordString)
        nonurlpasscode = encryptPassword(self.appObj.bcrypt, str(uuid.uuid4()), salt, self.safePasswordString)

        (failmessage, typeprivatevars, typepublicvars) = triggerTypeObj.activate(
            jobguid=jobguid,
            triggerType=triggerType,
            jobObj=jobObj,
            triggerOptions=triggerOptions,
            salt=salt,
            urlpasscode=urlpasscode,
            nonurlpasscode=nonurlpasscode
        )
        if failmessage is not None:
            return {"result": "Fail", "message": failmessage}, 404

        privateTriggerData = {
            "triggerActive": True,
            "type": triggerType,
            "salt": salt,
            "urlpasscode": urlpasscode,
            "nonurlpasscode": nonurlpasscode,
            "typeprivatevars": typeprivatevars,
            "typepublicvars": typepublicvars
        }

        jobObj.setNewPrivateTriggerData(privateTriggerData)

        self.appObj.appData['jobsData']._saveJobToObjectStore(str(jobObj.guid), store_connection)

        return jobObj._caculatedDict(self.appObj), 201

    def deactivateTrigger(self, jobguid):
        def dbfn(store_connection):
            return self.deactivateTriggerWithStoreConnection(
                store_connection=store_connection,
                jobguid=jobguid
            )
        return self.appObj.objectStore.executeInsideTransaction(dbfn)

    def deactivateTriggerWithStoreConnection(self, store_connection, jobguid):
        jobObj = self.appObj.appData['jobsData'].getJobRaw(jobguid)
        if jobObj is None:
            return {"result": "Fail", "message": "Job not found"}, 404
        if not jobObj.PrivateExternalTrigger["triggerActive"]:
            return {"result": "Warning", "message": "Trigger was not active"}, 400

        triggerType = jobObj.__dict__["PrivateExternalTrigger"]["type"]
        if triggerType not in self.TriggerTypes:
            print("ERROR!!! - type in data not found when deactivating job" + jobObj.__dict__["PrivateExternalTrigger"]["type"] + " Trying to continue")
        else:
            self.TriggerTypes[triggerType].deactivate(
                jobguid=jobguid,
                privateTriggerData=jobObj.PrivateExternalTrigger
            )

        privateTriggerData = {
            "triggerActive": False
        }

        jobObj.setNewPrivateTriggerData(privateTriggerData)
        self.appObj.appData['jobsData']._saveJobToObjectStore(str(jobObj.guid), store_connection)

        return jobObj._caculatedDict(self.appObj), 201
