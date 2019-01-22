#coding=utf-8

# Author: Ron Lin
# Date: 2017/11/25
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
from .serializer import ValidateRuleSerializer, ProcessorSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import ProjectSerializer
from django.contrib.auth.decorators import login_required
from rhino.util.handle_msg import handle_msg
from rhino.util.handle_msg import Message
from django.db import transaction
from .models import Processor, Crawler, Task
import os
import shutil
from crawler_manage.platforms.rhino_streaming_util import RhinoStreamingUtil
from rhino.util.general_response import ApiGeneralResponse


@login_required(login_url='/')
def processor_list(request, **kwargs):
    model = handle_msg(kwargs)
    project_ids = Project.objects.values_list('code', 'code', 'project_name')
    model['project_ids'] = project_ids
    return render(request, 'html/processor_list.html', model)


@login_required(login_url='/')
def processor_create(request, **kwargs):
    model = handle_msg(kwargs)
    return render(request, 'html/processor_create.html', model)


#修改processor
@login_required(login_url='/')
def processor_edit(request, processor_id, **kwargs):
    model = handle_msg(kwargs)
    processor = Processor.objects.get(id=processor_id)
    processor_obj = ProcessorSerializer(processor, many=False).data
    try:
        validate_rules = ValidateRule.objects.filter(task_id=processor_id)
        validate_rules_ser = ValidateRuleSerializer(validate_rules, many=True).data
        processor_obj['validate_rules'] = json.dumps(validate_rules_ser)
    except Exception as e:
        pass

    model['form'] = processor_obj
    return render(request, 'html/processor_edit.html', model)


@login_required(login_url='/')
@api_view(["GET"])
def processor_tasks(request, processor_id):
    crawlers = Crawler.objects.filter(processor_id=processor_id)
    try:
        if crawlers:
            return Response({
                "code": True,
                "msg": '请先删除相关联的爬虫，才能删除清洗程序。',
                "crawlers": len(crawlers)
            })
        else:
            return Response({
                "code": True,
                "msg": '确定要删除清洗程序？',
                "crawlers": len(crawlers)
            })
    except Exception as e:
        return Response({
            "code": False,
            "msg": '获取相关爬虫时出问题了',
            "crawlers": len(crawlers)
        })

@login_required(login_url='/')
@api_view(["GET"])
def processor_delete(request, processor_id):
    try:
        processor = Processor.objects.get(id=processor_id)
    except:
        raise Exception("Processor id %s is not existed" % processor_id)
    crawlers = Crawler.objects.filter(processor_id=processor_id)
    if crawlers:
        return Response({
            "code": False,
            "msg": '删除清洗程序失败,请先删除相关联的爬虫，才能删除清洗程序。',
            "crawlers": len(crawlers)
        })
    else:
        try:
            processor.delete()
            return Response({
                "code": True,
                "msg": '删除清洗程序成功',
                "crawlers": len(crawlers)
            })
        except:
            return Response({
                "code": False,
                "msg": 'id为{}的清洗程序删除失败'.format(processor_id),
                "crawlers": len(crawlers)
            })

@login_required(login_url='/')
@transaction.atomic
def processor_create_submit(request, **kwargs):
    model = {}
    crawler_app_folder = "/etc/rhino/crawler_app"
    success = True
    if request.method == 'POST':
        processor_id = request.POST.get('processor_id')
        processor_name = request.POST.get('processor_name')
        project_id = request.POST.get('project_id')
        project_name = request.POST.get('project_name')
        clean_app = request.FILES.get('clean_app', None)
        clean_parameters = request.POST.get('clean_parameters', None)
        field_mapping = request.POST.get('field_mapping', '')
        field_mapping = field_mapping.replace('\n', '')
        field_mapping = field_mapping.replace('', '')
        validate_rules_str = request.POST.get('validate_rules', '')
        deploy_target = request.POST.get('deploy_target', '')

        try:
            #判断编码相同的是否存在
            processors = Processor.objects.filter(id=processor_id)
            if processors and len(processors) > 0:
                return processor_create(request=request, msg="相同编码的清洗程序已经存在，请更换编码。", msg_type="error")

            crawlers = Crawler.objects.filter(id=project_id)
            if crawlers and len(crawlers) > 0:
                return processor_create(request=request, msg="清洗程序编码不能与现有的爬虫编码相同，请更换编码。", msg_type="error")

            tasks = Task.objects.filter(id=project_id)
            if tasks and len(tasks) > 0:
                return processor_create(request=request, msg="清洗程序编码不能与现有的任务编码相同，请更换编码。", msg_type="error")

            #如果目录已经存在，则删除重新建
            path = crawler_app_folder + '/' + processor_id
            if os.path.exists(path):
                shutil.rmtree(path)
            os.makedirs(path)

            # 上传文件
            if clean_app and clean_app.name:
                clean_app_dest = open(os.path.join(path, clean_app.name), 'wb+')
                for chunks in clean_app.chunks():
                    clean_app_dest.write(chunks)
                clean_app_file_name = crawler_app_folder + '/' + processor_id + '/' + clean_app.name
            else:
                return processor_create(request=request, msg="请上传清洗程序", msg_type="error")

            #存储验证规则
            validate_rules = json.loads(validate_rules_str)
            for rule in validate_rules:
                ValidateRule(task_id=processor_id, field_name=rule['field_name'],
                             rule=rule['rule'], type=rule['type'], desc=rule['desc']).save()

            processor = Processor(id=processor_id, project_id=project_id, project_name=project_name,
                                  processor_name=processor_name, clean_app=clean_app_file_name,
                                  clean_parameters=clean_parameters, fields_mapping=field_mapping,
                                  deploy_target=deploy_target,general_clean_rules=validate_rules_str)
            processor.save()

            return processor_list(request=request, msg="创建通用清洗程序成功", msg_type="success")

        except Exception as e:
            return processor_create(request=request, msg=str(e), msg_type="error")


@login_required(login_url='/')
@transaction.atomic
def processor_edit_submit(request, **kwargs):
    model = {}
    crawler_app_folder = "/etc/rhino/crawler_app"
    success = True
    if request.method == 'POST':
        processor_id = request.POST.get('processor_id')
        processor_name = request.POST.get('processor_name')
        project_id = request.POST.get('project_id')
        project_name = request.POST.get('project_name')
        clean_app = request.FILES.get('clean_app', None)
        clean_parameters = request.POST.get('clean_parameters', None)
        field_mapping = request.POST.get('field_mapping', '')
        field_mapping = field_mapping.replace('\n', '')
        field_mapping = field_mapping.replace('', '')
        validate_rules_str = request.POST.get('validate_rules', '')
        deploy_target = request.POST.get('deploy_target', '')

        try:
            #判断编码相同的是否存在
            processor = Processor.objects.get(id=processor_id)

            # 上传文件
            if clean_app and clean_app.name:
                # 如果目录已经存在，则删除重新建
                path = crawler_app_folder + '/' + processor_id
                if os.path.exists(path):
                    shutil.rmtree(path)
                os.makedirs(path)

                clean_app_dest = open(os.path.join(path, clean_app.name), 'wb+')
                for chunks in clean_app.chunks():
                    clean_app_dest.write(chunks)
                clean_app_file_name = crawler_app_folder + '/' + processor_id + '/' + clean_app.name

                processor.clean_app = clean_app_file_name

            processor.clean_parameters = clean_parameters
            processor.fields_mapping = field_mapping
            processor.deploy_target = deploy_target
            processor.general_clean_rules = validate_rules_str
            processor.processor_name = processor_name

            processor.save()

            #更新验证规则
            ValidateRule.objects.filter(task_id=processor_id).delete()

            validate_rules = json.loads(validate_rules_str)
            for rule in validate_rules:
                ValidateRule(task_id=processor_id, field_name=rule['field_name'],
                             rule=rule['rule'], type=rule['type'], desc=rule['desc']).save()

            return processor_list(request=request, msg="修改通用清洗程序成功，需要重启才能生效。", msg_type="success")

        except Exception as e:
            return processor_create(request=request, msg=str(e), msg_type="error")


@login_required(login_url='/')
@api_view(['POST', 'GET'])
def processor_detail_api(request, processor_id):
    try:
        processor = Processor.objects.get(id=processor_id)
        processor_obj = ProcessorSerializer(processor, many=False).data
        validate_rules = ValidateRule.objects.filter(task_id=processor_id)
        validate_rules_ser = ValidateRuleSerializer(validate_rules, many=True).data
        processor_obj['validate_rules'] = validate_rules_ser
        return ApiGeneralResponse(code=True, msg='success', data=processor_obj).get_response()
    except:
        return ApiGeneralResponse(code=False, msg='通用处理程序不存在', data=None).get_response()


@login_required(login_url='/')
@api_view(['POST', 'GET'])
def processor_list_api(request):
    if request.method == 'POST':
        limit = request.POST.get('limit', '10')
        offset = request.POST.get('offset', '0')
        search_keyword = request.POST.get('search_keyword', '')
        project_id = request.POST.get('project_id', '')
        check_status_str = request.POST.get('check_status', 'true')
    elif request.method == 'GET':
        limit = request.GET.get('limit', '10')
        offset = request.GET.get('offset', '0')
        search_keyword = request.GET.get('search_keyword', '')
        project_id = request.GET.get('project_id', '')
        check_status_str = request.POST.get('check_status', 'true')

    if check_status_str == 'true':
        check_status = True
    else:
        check_status = False

    processors = Processor.objects.order_by('-update_time')

    if project_id != '':
        processors = processors.filter(project_id=project_id)
    if search_keyword != '':
        processors = processors.filter(processor_name__contains=search_keyword)

    total_size = processors.count()

    if limit == '-1':
        limit = '10'

    processors = processors[int(offset): int(offset) + int(limit)]

    processors_obj = ProcessorSerializer(processors, many=True).data

    # for task in tasks_obj:
    #     pyspider = PyspiderUtil(server=PYSPIDER_SERVER, port=PYSPIDER_PORT)
    #     status = pyspider.check_status(task['id'])
    #     task['status'] = 0 if status == 0 or status ==1 or status ==4 else 1

    ## 如果不检查状态，则默认给值
    if check_status:
        statuses = RhinoStreamingUtil.check_status(processors)

    for processor in processors_obj:
        if check_status:
            status = 1 if statuses[processor['id']] is True else 0
            processor['clean_app_status'] = status
        else:
            processor['clean_app_status'] = 0

    return Response({
        "data": processors_obj,
        "size": total_size
    })


@login_required(login_url='/')
@api_view(['GET'])
def processor_start(request, processor_id):
    try:
        processor = Processor.objects.get(id=processor_id)
    except:
        raise Exception("Processor id %s is not existed" % processor_id)

    if RhinoStreamingUtil.check_status_for_single_task(processor) is True:
        return ApiGeneralResponse(code=False, msg="清洗已经在运行！").get_response()

    RhinoStreamingUtil.start_clean_deploy(processor)
    return ApiGeneralResponse(code=True).get_response()


@login_required(login_url='/')
@api_view(['GET'])
def processor_stop(request, processor_id):
    try:
        processor = Processor.objects.get(id=processor_id)
    except:
        raise Exception("Processor id %s is not existed" % processor_id)

    if RhinoStreamingUtil.check_status_for_single_task(processor) is False:
        return ApiGeneralResponse(code=False, msg="清洗已经停止运行！").get_response()

    RhinoStreamingUtil.stop_program(processor)
    return ApiGeneralResponse(code=True).get_response()
