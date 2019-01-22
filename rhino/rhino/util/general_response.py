#coding=utf-8

# Author: Ron Lin
# Date: 2017/9/21
# Email: hdsmtiger@gmail.com

from rest_framework.response import Response


class ApiGeneralResponse:

    def __init__(self, code=True, msg="No Msg", data=None):
        self.code = code
        self.msg = msg
        self.data = data

    def get_response(self):
        return Response({
            "code": self.code,
            "msg": self.msg,
            "data": self.data
        })

