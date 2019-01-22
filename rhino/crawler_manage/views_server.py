#coding=utf-8

# Author: Ron Lin
# Date: 2017/9/26
# Email: hdsmtiger@gmail.com

from django.shortcuts import render
from .models import SpiderServer
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rhino.util.general_response import ApiGeneralResponse
from .serializer import SpiderServerSerializer
from rest_framework.response import Response
from rhino.util.handle_msg import handle_msg

@login_required(login_url='/')
def create_server(request, **kwargs):
    model = handle_msg(kwargs)
    return render(request, 'html/server_create.html', model)


@login_required(login_url='/')
@api_view(['POST'])
def create_server_submit(request):

    if request.method == 'POST':
        host = request.POST.get('host', '')
        port_st = request.POST.get('port', '')
        port = int(port_st)
        type = request.POST.get('type', '')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        try:
            SpiderServer(host=host, port=port, type=type, username=username, password=password).save()
        except Exception as e:
            return ApiGeneralResponse(code=False, msg=str(e)).get_response()

    return ApiGeneralResponse(code=True, msg="新建爬虫服务器成功").get_response()


@login_required(login_url='/')
def list_server(request, **kwargs):
    model = handle_msg(kwargs)
    return render(request, 'html/server_list.html', model)


@login_required(login_url='/')
@api_view(['POST', 'GET'])
def list_server_api(request):
    if request.method == 'POST':
        limit = request.POST.get('limit', 10)
        offset = request.POST.get('offset',0)
        servers = SpiderServer.objects
        count = servers.count()
        servers = servers.order_by('-update_time')[int(offset):int(offset)+int(limit)]
        serializer = SpiderServerSerializer(servers, many=True)
        res = {
            "data": serializer.data,
            "size": count
        }
        return Response(res)

