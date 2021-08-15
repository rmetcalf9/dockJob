# API for saving up to 10 random numbers in memory
# This is used by various moniroting check processes to verfy that events are working.
from flask import request
from flask_restx import Resource, fields, apidoc, marshal
from werkzeug.exceptions import BadRequest, Conflict, InternalServerError, NotFound, Forbidden, Unauthorized
import uuid

def requiredInPayload(content, fieldList):
  for a in fieldList:
    if a not in content:
      raise BadRequest(a + ' not in payload')
    if content[a] is None:
      raise BadRequest(a + ' should not be empty')

def getPostNumberModel(appObj):
  return appObj.flastRestPlusAPIObject.model('postNumberModel', {
    'value': fields.String(default=None, description='Number Value')
  })

def getResultsModel(appObj):
  return appObj.flastRestPlusAPIObject.model('resultsModel', {
    #'value': fields.String(default='DEFAULT', description='Number Value')
  })

def checkCredentials(appObj, requestRecieved):
  if "Authorization" not in requestRecieved.headers:
    raise Unauthorized
  if not requestRecieved.headers["Authorization"].startswith("Basic "):
    raise Unauthorized
  if appObj.monitorCheckTempState.auth(username=requestRecieved.authorization["username"], password=requestRecieved.authorization["password"]):
    return
  raise Forbidden

def checkValidUuid(uuidStr):
  try:
    val = uuid.UUID(uuidStr, version=4)
  except ValueError:
    raise BadRequest


def registerAPI(appObj, APInamespace):
  @APInamespace.route('/<string:uuidStr>')
  class MonitorCheckTempState(Resource):
    '''monitorCheckTempState'''

    @APInamespace.doc('Save a number')
    @APInamespace.expect(getPostNumberModel(appObj))
    @appObj.flastRestPlusAPIObject.response(400, 'Validation error')
    @appObj.flastRestPlusAPIObject.response(200, 'Success')
    @appObj.flastRestPlusAPIObject.marshal_with(getResultsModel(appObj), code=200, description='Post Number', skip_none=True)
    @APInamespace.response(403, 'Forbidden')
    def post(self, uuidStr):
      '''Post Number'''
      content_raw = request.get_json()
      content = marshal(content_raw, getPostNumberModel(appObj))
      requiredInPayload(content, ['value'])

      checkCredentials(appObj, request)
      checkValidUuid(uuidStr)

      raise BadRequest("value must be a number")

      try:
        pass
      except Exception as err:
        raise err

    @APInamespace.doc('Get a number')
    @APInamespace.marshal_with(getResultsModel(appObj))
    @APInamespace.response(200, 'Success', model=getResultsModel(appObj))
    @APInamespace.response(401, 'Unauthorized')
    @APInamespace.response(403, 'Forbidden')
    @APInamespace.response(404, 'User Not Found')
    def get(self, uuidStr):
      '''Get number'''
      checkCredentials(appObj, request)
      checkValidUuid(uuidStr)

      try:
        retVal = {"value": "123"}
        return retVal
      except Logic.LogicException as e:
        raise BadRequest(str(e))
      except MultiTenantObjectStore.InvalidTenantNameException as e:
        raise BadRequest(str(e))
      except ClientError as e:
        print("boto Client")
        print(" tenantName:", tenantName)
        raise e
