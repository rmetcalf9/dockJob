from flask_restx import Resource
from flask import request

def register_api(flaskObj, externalTriggerManager):
    ns = flaskObj.namespace('', description='External Trigger')

    @ns.route('/up')
    class check(Resource):
        '''Check on server'''

        def get(self):
            '''Simple check'''
            return { "result": "Success" }

    @ns.route('/trigger/<string:urlid>')
    class trigger(Resource):
        '''Trigger the notification'''

        def post(self, urlid):
            '''Simple check'''
            return externalTriggerManager.processTrigger(urlid, request.headers, request.data)
