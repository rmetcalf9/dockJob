from flask_restplus import Resource
from JobExecution import getJobExecutionModel
from flask import request


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

