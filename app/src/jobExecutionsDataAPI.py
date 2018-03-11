from flask_restplus import Resource
from JobExecution import getJobExecutionModel
from flask import request
from werkzeug.exceptions import BadRequest


def registerAPI(appObj):
  nsJobExecutions = appObj.flastRestPlusAPIObject.namespace('executions', description='Job Executions')
  @nsJobExecutions.route('/')
  class executionList(Resource):
    '''Operations relating to jobs'''

    @nsJobExecutions.doc('getexecutions')
    @nsJobExecutions.marshal_with(appObj.getResultModel(getJobExecutionModel(appObj)))
    @appObj.flastRestPlusAPIObject.response(200, 'Success')
    @nsJobExecutions.param('offset', 'Number to start from')
    @nsJobExecutions.param('pagesize', 'Results per page')
    @nsJobExecutions.param('query', 'Search Filter')
    def get(self):
      '''Get Job Executions'''
      def outputJobExecution(item):
        return item
      def filterJobExecution(item, whereClauseText):
        return True
      return appObj.getPaginatedResult(
        appObj.jobExecutor.getAllJobExecutions(None),
        outputJobExecution,
        request,
        filterJobExecution
      )

  @nsJobExecutions.route('/<string:guid>')
  @nsJobExecutions.response(400, 'Job Execution not found')
  @nsJobExecutions.param('guid', 'Job Execution identifier')
  class job(Resource):
    '''Show a single execution Job'''
    @nsJobExecutions.doc('get_jobexecution')
    @nsJobExecutions.marshal_with(getJobExecutionModel(appObj))
    def get(self, guid):
      '''Fetch a given resource'''
      execution = appObj.jobExecutor.getJobExecutionStatus(guid)
      if execution is None:
        raise BadRequest('Invalid Job Execution Identifier')
      return execution

