#coding=utf-8

# Author: Ron Lin
# Date: 2017/10/2
# Email: hdsmtiger@gmail.com


def handle_msg(kwargs):
    if kwargs is None:
        return {}

    if 'msg_type' in kwargs:
        msg_type = kwargs["msg_type"]
    else:
        msg_type = "success"

    if 'msg' in kwargs:
        return Message(msg=kwargs['msg'], msg_type=msg_type).get()

    return {}


def add_message(model, msg, msg_type="success"):
    model["message"] = {
        "msg": msg,
        "msg_type": msg_type
    }
    return model

class Message:

    def __init__(self, msg, msg_type="success"):
        self.__msg = msg
        self.__msg_type = msg_type

    def get(self):
        return {
            "message": {
                "msg": self.__msg,
                "msg_type": self.__msg_type
            }
        }
