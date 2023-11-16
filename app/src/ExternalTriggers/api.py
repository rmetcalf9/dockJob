from flask_restx import Resource

def register_api(flaskObj, appObj):
    ns = flaskObj.namespace('', description='External Trigger')

    @ns.route('/up')
    class check(Resource):
        '''Check on server'''

        def get(self):
            '''Simple check'''
            return { "result": "Success" }

