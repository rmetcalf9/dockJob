# This is the private API
# it appears on the normal API endpoint
from flask_restx import Resource, marshal
from flask import request
from werkzeug.exceptions import BadRequest
from APIModels import getJobModel, getErrorModel

def requiredInPayload(content, fieldList):
  for a in fieldList:
    if a not in content:
      raise BadRequest(a + ' not in payload')
    if content[a] is None:
      raise BadRequest(a + ' should not be empty')

def register_private_api(flaskObj, externalTriggerManager):
    ns = flaskObj.namespace('jobs', description='External Trigger Private API endpoints (under /api)')

    @ns.route('/<string:jobguid>/activateTrigger')
    class activateTrigger(Resource):
        '''Setus up a trigger if ther is on already there it will replace it'''

        @ns.doc('activate_trigger_on_job')
        def post(self, jobguid):
            '''Activate Trigger'''
            reuqestJson = request.get_json()
            requiredInPayload(reuqestJson, ['triggerType', 'triggerOptions'])
            (resp, status) =  externalTriggerManager.activateTrigger(jobguid, reuqestJson["triggerType"], reuqestJson["triggerOptions"])
            if status > 199:
                if status < 300:
                    return marshal(resp, getJobModel(flaskObj)), status
            return marshal(resp, getErrorModel(flaskObj)), status

    @ns.route('/<string:jobguid>/deactivateTrigger')
    class deactivateTrigger(Resource):
        '''deactivates a trigger'''

        @ns.doc('deactivate_trigger_on_job')
        def post(self, jobguid):
            '''Acrivate Trigger'''
            raise Exception("NI")
            # (resp, status) =  externalTriggerManager.deactivateTrigger(jobguid, reuqestJson["triggerType"], reuqestJson["triggerOptions"])
            # if status > 199:
            #     if status < 300:
            #         return marshal(resp, getJobModel(flaskObj)), status
            # return marshal(resp, getErrorModel(flaskObj)), status
