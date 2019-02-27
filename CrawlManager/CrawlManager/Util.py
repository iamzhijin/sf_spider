import json

class Util():

    def success_result(self, msg='success', data=None):
        result = {
            'message': msg,
            'flag': '000',
            'data': [data]
        }
        return json.dumps(result)

    def fail_result(self, msg='fail', code='001', data=None):
        result = {
            'message': msg,
            'flag': code,
            'data': data
        }
        return json.dumps(result)    
      