#coding=utf-8

# Author: Ron Lin
# Date: 2017/9/17
# Email: hdsmtiger@gmail.com

from django.shortcuts import render
from .models import ValidateRule
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Crawler
from .models import Project
from .models import Task, Processor, ValidateRule
import json,logging
from .serializer import TaskSerializer
from django.db import transaction
from .platforms.pyspider_util import PyspiderUtil
from django.contrib.auth.decorators import login_required
from rhino.util.general_response import ApiGeneralResponse
from crawler_manage.platforms.rhino_streaming_util import RhinoStreamingUtil
from .models import ValidateRule
from .serializer import ValidateRuleSerializer, CrawlerSerializer
from rhino.settings import PYSPIDER_SERVER, PYSPIDER_PORT
from .models import SpiderServer
from .serializer import SpiderServerSerializer
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from rhino.util.handle_msg import handle_msg
from .models import TaskServer
from crawler_manage.platforms.pyspider_util import compose_pyspider_task_name
# from django.views.decorators.csrf import csrf_exempt,csrf_protect
@login_required(login_url='/')
def task_create(request, **kwargs):
    servers = SpiderServer.objects.all().order_by('-update_time')
    spider_servers = SpiderServerSerializer(servers, many=True).data
    model = handle_msg(kwargs)
    model['spider_servers'] = spider_servers
    if request.method == 'POST':
        crawler_id = request.POST.get('crawler_id', '')
    elif request.method == 'GET':
        crawler_id = request.GET.get('crawler_id', '')
    if crawler_id and len(crawler_id)>0:
        crawlers = Crawler.objects.get(pk=crawler_id)
        crawler_obj = CrawlerSerializer(crawlers, many=False).data
        if crawler_obj and crawler_obj['clean_method'] == 'common':
            processor = Processor.objects.get(id=crawler_obj['processor_id'])
            crawler_obj['deploy_target'] = processor.deploy_target
            validate_rules = ValidateRule.objects.filter(task_id=crawlers.processor_id)
            validate_rules_ser = ValidateRuleSerializer(validate_rules, many=True).data
            crawler_obj['validate_rules'] = json.dumps(validate_rules_ser)
            model["crawler_data"] = crawler_obj

    return render(request, 'html/task_create.html', model)

@login_required(login_url='/')
def task_edit(request, task_id, **kwargs):
    model = handle_msg(kwargs)
    task = Task.objects.get(id=task_id)
    tasks_obj = TaskSerializer(task, many=False).data
    try:
        validate_rules = ValidateRule.objects.filter(task_id=task_id)
        validate_rules_ser = ValidateRuleSerializer(validate_rules, many=True).data
        tasks_obj['validate_rules'] = json.dumps(validate_rules_ser)
    except Exception as e:
        pass

    taskServers = TaskServer.objects.filter(task=task)
    task_servers = []
    for taskServer in taskServers:
        task_servers.append(taskServer.server_id)
    tasks_obj['task_servers'] = task_servers
    servers = SpiderServer.objects.all().order_by('-update_time')
    spider_servers = SpiderServerSerializer(servers, many=True).data
    model['form'] = tasks_obj
    model['spider_servers'] = spider_servers
    return render(request, 'html/task_edit.html', model)

@login_required(login_url='/')
def task_log(request, task_id, **kwargs):

    return render(request, 'html/task_log.html', {
        "task_id":task_id
    })

@login_required(login_url='/')
@transaction.atomic
def task_edit_submit(request):
    if request.method == 'POST':
        validate_rules_str = request.POST.get('validate_rules', '')
        deploy_target = request.POST.get('deploy_target', '')
        servers = request.POST.getlist('servers', None)
        task_id = request.POST.get('task_id', None)

        if task_id is None or len(task_id) <= 0:
            return task_list(request=request, msg="任务ID找不到", msg_type="error")

        if servers is None or len(servers) <= 0:
            return task_edit(request=request, task_id=task_id, msg="请选择爬虫服务器", msg_type="error")

        try:
            task = Task.objects.get(id=task_id)
        except :
            return task_list(request=request, msg="任务ID找不到", msg_type="error")

        task.deploy_target = deploy_target
        task.save()

        # 清空再保存validate rules
        current_validate_rules = ValidateRule.objects.filter(task_id=task_id)
        for current_validate_rule in current_validate_rules:
            current_validate_rule.delete()
        validate_rules = json.loads(validate_rules_str)
        for rule in validate_rules:
            ValidateRule(task_id=task_id, field_name=rule['field_name'],
                 rule=rule['rule'], type=rule['type'], desc=rule['desc']).save()

        # 清空再保存servers
        # 暂停所有的爬虫任务，否则会导致游离的服务
        running_servers = TaskServer.objects.filter(task=task)
        for running_server in running_servers:
            if str(running_server.server_id) in servers and running_server.task_id == task_id:
                pass
            else:
                crawler_stop(request, running_server.id)
            running_server.delete()
        for server_id in servers:
            server = SpiderServer.objects.get(pk=server_id)
            TaskServer(task=task, server=server).save()

        return task_list(request, msg="保存任务成功！", msg_type="success")

    return redirect(reverse("crawler_manage:task_list"))


@login_required(login_url='/')
@transaction.atomic
def task_create_submit(request):
    if request.method == 'POST':
        validate_rules_str = request.POST.get('validate_rules', '')
        crawler_id = request.POST.get('crawler_id', '')
        crawler_parameters = request.POST.get('crawler_parameters', '')
        clean_parameters = request.POST.get('clean_parameters', '')
        deploy_target = request.POST.get('deploy_target', '')
        servers = request.POST.getlist('servers', None)
        # servers = request.POST.getlist('servers', None)
        if len(crawler_id) <= 0:
            return task_create(request=request, msg="爬虫编码不存在", msg_type="error")

        if servers is None or len(servers) <= 0:
            return task_create(request=request, msg="请选择爬虫服务器", msg_type="error")

        crawler = Crawler.objects.get(id=crawler_id)
        task_id = crawler_id + '_' + str(Task.objects.filter(id__startswith=crawler_id).count() + 1)
        task = Task(id=task_id, crawler_id=crawler.id, crawler_name=crawler.crawler_name,
                    project_id=crawler.project_id, project_name=crawler.project_name,
                    crawler_app=crawler.crawler_app, crawler_parameters=crawler_parameters,
                    clean_app=crawler.clean_app, clean_parameters=clean_parameters,
                    fields_mapping=crawler.fields_mapping, deploy_target=deploy_target, general_clean_rules="",
                    status=0, start_time=None, stop_time=None, servers="",
                    clean_method=crawler.clean_method, processor_id=crawler.processor_id,
                    processor_name=crawler.processor_name)
        task.save()

        validate_rules = json.loads(validate_rules_str)
        for rule in validate_rules:
            ValidateRule(task_id=task_id, field_name=rule['field_name'],
                         rule=rule['rule'], type=rule['type'], desc=rule['desc']).save()

        for server_id in servers:
            server = SpiderServer.objects.get(pk=server_id)
            TaskServer(task=task, server=server).save()

        return task_list(request, msg="新建任务成功！", msg_type="success")

    return redirect(reverse("crawler_manage:task_create"))



@login_required(login_url='/')
def task_list(request, **kwargs):
    model = handle_msg(kwargs)
    project_ids = Project.objects.values_list('code', 'code', 'project_name')
    model['project_ids'] = project_ids
    return render(request, 'html/task_list.html', model)


@login_required(login_url="/")
@api_view(["POST", "GET","DELETE"])
def task_detail_api(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == 'DELETE':
        task.delete()
        from rest_framework import status
        return Response(status=status.HTTP_204_NO_CONTENT)
    tasks_obj = TaskSerializer(task, many=False).data
    try:
        validate_rules = ValidateRule.objects.filter(task_id=task_id)
        validate_rules_ser = ValidateRuleSerializer(validate_rules, many=True).data
        tasks_obj['validate_rules'] = validate_rules_ser
    except Exception as e:
        pass

    return ApiGeneralResponse(code=True, data=tasks_obj).get_response()

@login_required(login_url="/")
@api_view(["GET"])
@transaction.atomic
def task_delete(request, task_id):
    task = Task.objects.get(id=task_id)
    # logging.warning(task.clean_method)
    try:
        # 如果清洗程序是自定义程序,就暂停清洗程序
        stop = True
        if task.clean_method == 'custom':
            # logging.warning('这个清洗程序是自定义清洗程序')
            stop = stop_clean(task_id)
        if stop:
            logging.warning('清洗程序删除成功')
            # 获取validate_rules
            validate_rules = ValidateRule.objects.filter(task_id=task_id)

            # 获取taskservers,并把相关的pyspider爬虫任务删除
            task_servers = TaskServer.objects.filter(task_id=task_id)
            server_ids = [task_server.id for task_server in task_servers]
            for server_id in server_ids:
                delete_crawler(str(server_id))
            # 删除rules
            validate_rules.delete()
            # 删除servers
            task_servers.delete()
            # 删除任务
            task.delete()
            return Response({
                "code": True,
                "msg": '任务id为{}的任务删除成功'.format(task_id)
            })
        else:
            logging.warning('清洗程序删除失败')
            return Response({
                "code": False,
                "msg": '任务id为{}的任务删除失败'.format(task_id)
            })
    except Exception as e:
        logging.warning(e)
        return Response({
            "code": False,
            "msg": '任务id为{}的任务删除失败'.format(task_id)
        })

@login_required(login_url='/')
@api_view(['POST', 'GET'])
def task_list_api(request):
    if request.method == 'POST':
        limit = request.POST.get('limit', '10')
        offset = request.POST.get('offset', '0')
        search_keyword = request.POST.get('search_keyword', '')
        project_id = request.POST.get('project_id', '')
    elif request.method == 'GET':
        limit = request.GET.get('limit', '-1')
        offset = request.GET.get('offset', '0')
        search_keyword = request.GET.get('search_keyword', '')
        project_id = request.GET.get('project_id', '')

    tasks = Task.objects.order_by('-update_time')

    if project_id != '':
        tasks = tasks.filter(project_id=project_id)
    if search_keyword != '':
        tasks = tasks.filter(crawler_name__contains=search_keyword)

    total_size = tasks.count()

    if limit == '-1':
        limit = '10'

    tasks = tasks[int(offset): int(offset) + int(limit)]

    tasks_obj = TaskSerializer(tasks, many=True).data

    # for task in tasks_obj:
    #     pyspider = PyspiderUtil(server=PYSPIDER_SERVER, port=PYSPIDER_PORT)
    #     status = pyspider.check_status(task['id'])
    #     task['status'] = 0 if status == 0 or status ==1 or status ==4 else 1

    statuses = RhinoStreamingUtil.check_status(tasks)
    for task in tasks_obj:
        status = 1 if statuses[task['id']] is True else 0
        task['clean_app_status'] = status

    return Response({
        "data": tasks_obj,
        "size": total_size
    })

@login_required(login_url='/')
@api_view(['GET', 'POST'])
def task_status_api(request, task_id):
    if task_id is None:
        return ApiGeneralResponse(code=False, msg="任务ID不存在！").get_response()

    task = Task.objects.get(id=task_id)
    servers = TaskServer.objects.filter(task=task)
    statuses = []
    for server in servers:
        pyspider = PyspiderUtil(server=server.server.host, port=server.server.port)
        try:
            task_id = server.task.id
            if task.clean_method == 'common':
                task_id = server.task.processor_id
            status = pyspider.check_status(compose_pyspider_task_name(task_id=task_id,
                                                                  project_code=server.task.project_id,
                                                                  crawler_code=server.task.crawler_id))
        except:
            status = 0
        statuses.append({
            "id": server.id,
            "host": server.server.host,
            "port": server.server.port,
            "status": 0 if status == 0 or status ==1 or status ==4 else 1
        })

    return ApiGeneralResponse(code=True, msg="获取成功！", data=statuses).get_response()


@login_required(login_url='/')
@api_view(['GET'])
def crawler_start(request, task_server_id, rate=1, burst=3):
    try:
        task_server = TaskServer.objects.get(pk=task_server_id)
    except Exception as e:
        return Response({
            "code": False,
            "msg": "Task Server id " + task_server_id + " 不存在！"
        })

    crawler_app = task_server.task.crawler_app

    pyspider = PyspiderUtil(server=task_server.server.host, port=task_server.server.port)
    task_id = task_server.task.id
    if task_server.task.clean_method == 'common':
        task_id = task_server.task.processor_id
    pyspider_task_name = compose_pyspider_task_name(task_id=task_id,
                               project_code=task_server.task.project_id,
                               crawler_code=task_server.task.crawler_id)

    try:
        status = pyspider.check_status(pyspider_task_name)
    except Exception as e:
        #status = 4
        return ApiGeneralResponse(code=False, msg="服务器查看任务状态失败，请检查服务器是否正常运行").get_response()
    if status == 4: #系统中没找到
        try:
            file_object = open(crawler_app, 'r')
            code = file_object.read()
            res = pyspider.submit_task(code, pyspider_task_name)
            if res is True:
                res = pyspider.start_task(pyspider_task_name)
                if res is True:
                    response = Response({
                    "code": True,
                    "msg": "任务" + pyspider_task_name + "提交到pyspider成功！"
                })
                else:
                    response = Response({
                        "code": False,
                        "msg": "任务" + pyspider_task_name + "启动失败"
                    })
            else:
                response = Response({
                    "code": False,
                    "msg": "任务" + pyspider_task_name + "提交到pyspider失败！"
                })
        finally:
            file_object.close()
    elif status == 0 or status == 1: #停止状态
        res = pyspider.start_task(pyspider_task_name)
        if res is True:
            response = Response({
                "code": True,
                "msg": "任务" + pyspider_task_name + "提交到pyspider成功！"
            })
        else:
            response = Response({
                "code": False,
                "msg": "任务" + pyspider_task_name + "启动失败"
            })
    elif status == 2: #已经启动
        response = Response({
            "code": False,
            "msg": "任务" + pyspider_task_name + "已经启动！"
        })
    elif status == 3: #状态未知
        response = Response({
            "code": False,
            "msg": "任务" + pyspider_task_name + "状态未知，请稍后重试！"
        })
    else:
        response = Response({
            "code": False,
            "msg": "任务" + pyspider_task_name + "状态未知，请稍后重试！ pyspider状态码: " + status
        })


    # 更新数据库状态
    #if response.data['code'] is True:
    #    task.status = 1
    #    task.save()
    #else:
    #    task.status = 0
    #    task.save()

    return response



@login_required(login_url='/')
@api_view(['GET'])
def crawler_stop(request, task_server_id):
    try:
        task_server = TaskServer.objects.get(pk=task_server_id)
    except Exception as e:
        return Response({
            "code": False,
            "msg": "Task id " + task_server_id + " 不存在！"
        })

    crawler_app = task_server.task.crawler_app
    pyspider = PyspiderUtil(server=PYSPIDER_SERVER, port=PYSPIDER_PORT)
    task_id = task_server.task.id
    if task_server.task.clean_method == 'common':
        task_id = task_server.task.processor_id
    pyspider_task_name = compose_pyspider_task_name(task_id=task_id,
                                                    project_code=task_server.task.project_id,
                                                    crawler_code=task_server.task.crawler_id)
    status = pyspider.check_status(pyspider_task_name)
    if status == 4: #系统中没找到
        response = Response({
            "code": False,
            "msg": "任务" + pyspider_task_name + "没有找到！"
        })
    elif status == 2: #启动
        res = pyspider.stop_task(pyspider_task_name)
        if res is True:
            response = Response({
                "code": True,
                "msg": "任务" + pyspider_task_name + "关闭成功！"
            })
        else:
            response = Response({
                "code": False,
                "msg": "任务" + pyspider_task_name + "关闭失败！"
            })
    else:
        response = Response({
            "code": True,
            "msg": "任务" + pyspider_task_name + "已经关闭！"
        })
    return response

@login_required(login_url='/')
@api_view(['GET'])
def backup_start(request, task_id):
    return ApiGeneralResponse(code=True).get_response()


@login_required(login_url='/')
@api_view(['GET'])
def backup_stop(request, task_id):
    return ApiGeneralResponse(code=True).get_response()


@login_required(login_url='/')
@api_view(['GET'])
def clean_start(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except:
        raise Exception("Task id %s is not existed" % task_id)

    if task.clean_method == 'common':
        task.id = task.processor_id

    if RhinoStreamingUtil.check_status_for_single_task(task) is True:
        return ApiGeneralResponse(code=False, msg="清洗已经在运行！").get_response()

    RhinoStreamingUtil.start_clean_deploy(task)
    return ApiGeneralResponse(code=True).get_response()


@login_required(login_url='/')
@api_view(['GET'])
def clean_stop(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except:
        raise Exception("Task id %s is not existed" % task_id)

    if task.clean_method == 'common':
        task.id = task.processor_id

    if RhinoStreamingUtil.check_status_for_single_task(task) is False:
        return ApiGeneralResponse(code=False, msg="清洗已经停止运行！").get_response()

    RhinoStreamingUtil.stop_program(task)
    return ApiGeneralResponse(code=True).get_response()


@api_view(['GET','DELETE'])
def get_validate_rules(request, task_id):
    if request.method == "GET":
        validate_rules = ValidateRule.objects.filter(task_id=task_id)
        serializer = ValidateRuleSerializer(validate_rules, many=True)
        return Response(serializer.data)
    if request.method == 'DELETE':
        validate_rules = ValidateRule.objects.filter(task_id=task_id)
        validate_rules.delete()
        from rest_framework import status
        return Response(status=status.HTTP_204_NO_CONTENT)

# 删掉pyspider爬虫任务
def delete_crawler(task_server_id):
    try:
        task_server = TaskServer.objects.get(pk=task_server_id)
    except Exception as e:
        return Response({
            "code": False,
            "msg": "Task id " + task_server_id + " 不存在！"
        })
    crawler_app = task_server.task.crawler_app
    pyspider = PyspiderUtil(server=PYSPIDER_SERVER, port=PYSPIDER_PORT)
    task_id = task_server.task.id
    if task_server.task.clean_method == 'common':
        task_id = task_server.task.processor_id
    pyspider_task_name = compose_pyspider_task_name(task_id=task_id,
                                                    project_code=task_server.task.project_id,
                                                    crawler_code=task_server.task.crawler_id)
    status = pyspider.check_status(pyspider_task_name)
    if status == 4: #系统中没找到
        response = Response({
            "code": False,
            "msg": "任务" + pyspider_task_name + "没有找到！"
        })
    elif status == 2: #启动
        res = pyspider.stop_task(pyspider_task_name)
        if res is True:
            response = Response({
                "code": True,
                "msg": "任务" + pyspider_task_name + "关闭成功！"
            })
        else:
            response = Response({
                "code": False,
                "msg": "任务" + pyspider_task_name + "关闭失败！"
            })
    else:
        response = Response({
            "code": True,
            "msg": "任务" + pyspider_task_name + "已经关闭！"
        })
    # 更改group为delete
    pyspider.delete_task(pyspider_task_name)




# 停掉清洗程序
def stop_clean(task_id):
    stop = False
    try:
        task = Task.objects.get(id=task_id)
    except:
        raise Exception("Task id %s is not existed" % task_id)

    if task.clean_method == 'common':
        task.id = task.processor_id

    if RhinoStreamingUtil.check_status_for_single_task(task) is False:
        logging.warning('清洗程序已经停止运行!')
        stop = True
        return stop
    try:
        RhinoStreamingUtil.stop_program(task)
        logging.warning('清洗程序停止运行成功了!')
        stop =True
    except Exception as e:
        logging.warning('清洗程序停止运行出错了!')
    return stop