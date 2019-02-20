import json

class Util():

    def success_result(self, msg='success', data=None):
        result = {
            'message': msg,
            'code': '000',
            'data': data
        }
        return json.dumps(result)

    def fail_result(self, msg='fail', code='001', data=None):
        result = {
            'message': msg,
            'code': code,
            'data': data
        }
        return json.dumps(result)    
      