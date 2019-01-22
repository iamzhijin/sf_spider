#coding=utf-8

# Author: Ron Lin
# Date: 2017/9/15
# Email: hdsmtiger@gmail.com

import json

from django.shortcuts import render
from django.shortcuts import get_object_or_404
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Project
from django.shortcuts import get_object_or_404
from .models import ValidateRule
from .serializer import ValidateRuleSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import ProjectSerializer
from django.contrib.auth.decorators import login_required
from rhino.util.handle_msg import handle_msg
from rhino.util.handle_msg import Message

@login_required(login_url='/')
def project_create(request, **kwargs):
    model = handle_msg(kwargs)
    form = {}
    if request.method == 'POST':
        id = request.POST['project_id']
        name = request.POST['project_name']
        desc = request.POST['project_desc']
        form = {
            "project_id": id,
            "project_name": name,
            "project_desc": desc
        }
        try:
            project = Project.objects.get(code=id)
        except Exception as e:
            project = Project(code=id, project_name=name, desc=desc)
            project.save()
            # todo 切换成详情页
            return project_list_page(request, msg="保存成功！")

        if project:
            model['form'] = form
            model['message'] = Message(msg='项目编码已经存在，无法保存！', msg_type='error').get()['message']

    return render(request, 'html/project_create.html', model)


@login_required(login_url='/')
def project_list_page(request, **kwargs):
    model = handle_msg(kwargs)
    return render(request, 'html/projects_list.html', model)


@login_required(login_url='/')
@api_view(['POST'])
def project_list_api(request):
    if request.method == 'POST':
        limit = request.POST['limit']
        offset = request.POST['offset']
        projects = Project.objects.order_by('-update_time')[int(offset):int(offset)+int(limit)]
        serializer = ProjectSerializer(projects, many=True)
        res = {
            "data": serializer.data,
            "size": Project.objects.all().count()
        }
        return Response(res)
