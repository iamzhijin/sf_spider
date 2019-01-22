# coding=utf-8

# Author: Ron Lin
# Date: 2017/9/16
# Email: hdsmtiger@gmail.com

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
from .models import Project, Processor, Crawler, ValidateRule,Task
import shutil
from .serializer import CrawlerSerializer, ValidateRuleSerializer
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.db import transaction
from rhino.util.handle_msg import handle_msg
from rhino.util.handle_msg import add_message
import time
from pygments import highlight
from pygments import lexers
from pygments import formatters
from .models import Task
import json



@login_required(login_url='/')
@transaction.atomic
def crawler_create(request, **kwargs):
    model = handle_msg(kwargs)

    crawler_app_folder = "/etc/rhino/crawler_app"
    form = {}
    success = True
    if request.method == 'POST':
        crawler_id = request.POST['crawler_id']
        project = request.POST['project']
        project_id = request.POST['project_id']
        project_name = request.POST['project_name']
        crawler_name = request.POST['crawler_name']
        crawler_app = request.FILES.get('crawler_app', None)
        clean_app = request.FILES.get('clean_app', None)
        clean_parameters = request.POST['clean_parameters']
        clean_method = request.POST.get('clean_method', 'custom')
        processor_id = request.POST.get('processor_id', '')
        processor_name = request.POST.get('processor_name', '')
        nc = "off"
        try:
            nc = request.POST['need_clean']
        except Exception as e:
            need_clean = False
        if nc and nc == 'on':
            need_clean = True
        else:
            need_clean = False

        try:

            # 清空目录
            path = crawler_app_folder + '/' + crawler_id
            if os.path.exists(path):
                shutil.rmtree(path)
            os.makedirs(path)


            if clean_method == 'common':
                processor = Processor.objects.get(id=processor_id)
                field_mapping = processor.fields_mapping
                clean_app_file_name = processor.clean_app
                clean_parameters = processor.clean_parameters
            else:
                field_mapping = request.POST.get('field_mapping', '')
                field_mapping = field_mapping.replace('\n', '')
                if clean_app and clean_app.name:
                    # 上传清洗文件
                    clean_app_dest = open(os.path.join(path, clean_app.name), 'wb+')
                    for chunks in clean_app.chunks():
                        clean_app_dest.write(chunks)
                    clean_app_file_name = crawler_app_folder + '/' + crawler_id + '/' + clean_app.name
                else:
                    clean_app_file_name = ""


            # 上传爬虫文件
            crawler_app_dest = open(os.path.join(path, crawler_app.name), 'wb+')
            for chunks in crawler_app.chunks():
                crawler_app_dest.write(chunks)

            crawler = Crawler.objects.filter(pk=crawler_id)
            if crawler:
                success = False
                add_message(model, "已经存在同样编码的爬虫", msg_type="error")
            else:
                crawler = Crawler(project_id=project_id, id=crawler_id, project_name=project_name,
                                  crawler_name=crawler_name,
                                  crawler_app=crawler_app_folder + '/' + crawler_id + '/' + crawler_app.name,
                                  clean_app=clean_app_file_name,
                                  clean_parameters=clean_parameters,
                                  need_clean=need_clean, fields_mapping=field_mapping,
                                  processor_id=processor_id, processor_name=processor_name,
                                  clean_method=clean_method)
                crawler.save()
        except Exception as e:
            add_message(model, str(e), msg_type="error")
            success = False

        if success is True:
            add_message(model, "新增爬虫成功")
            return crawler_list(request, msg="新增爬虫成功")
        else:
            form["crawler_id"] = crawler_id
            form["crawler_name"] = crawler_name
            form["project"] = project
            form["project_id"] = project_id
            form["project_name"] = project_name
            form["crawler_app"] = crawler_app
            form["clean_app"] = clean_app
            form["clean_parameters"] = clean_parameters
            if need_clean:
                form["need_clean"] = 'on'
            form["field_mapping"] = field_mapping
        model['form'] = form

    elif request.method == 'GET':
        project_id = request.GET.get('project', '')
        if project_id:
            project = Project.objects.get(code=project_id)
            form['project_id'] = project_id
            form['project_name'] = project.project_name
            form['project'] = project_id  + ' ---- ' + project.project_name
        model['form'] = form

    return render(request, 'html/crawler_create.html', model)

@login_required(login_url='/')
@api_view(["GET"])
def crawler_tasks(request, crawler_id):
    tasks = Task.objects.filter(crawler_id=crawler_id)
    try:
        if tasks:
            return Response({
                "code": True,
                "msg": '请先删除相关联的任务，才能删除爬虫。',
                "tasks": len(tasks)
            })
        else:
            return Response({
                "code": True,
                "msg": '确定要删除爬虫？',
                "tasks": len(tasks)
            })
    except Exception as e:
        return Response({
            "code": False,
            "msg": '获取爬虫任务的时候出问题了',
            "tasks": len(tasks)
        })

@login_required(login_url='/')
@api_view(["GET"])
def crawler_delete(request, crawler_id):
    try:
        crawler_item = Crawler.objects.get(id=crawler_id)
    except:
        return crawler_list(request, msg="爬field_mapping虫不存在")
    tasks = Task.objects.filter(crawler_id=crawler_id)
    if tasks:
        return Response({
            "code": False,
            "msg": '请先删除相关联的任务，才能删除爬虫。',
            "tasks": len(tasks)
        })
    else:
        try:
            crawler_item.delete()
            return Response({
                "code": True,
                "msg": '确定要删除爬虫?',
                "tasks": len(tasks)
            })
        except:
            return Response({
                "code": False,
                "msg": '爬虫id为{}的爬虫删除失败'.format(crawler_id),
                "tasks": len(tasks)
            })

@login_required(login_url='/')
def view_crawler_app(request, crawler_id):
    crawler_item = Crawler.objects.get(id=crawler_id)
    crawler_app = crawler_item.crawler_app

    try:
        code_text = ''
        file_object = open(crawler_app, 'r')
        for line in file_object:
            code_text = code_text + line
    finally:
        file_object.close()


    highted_code = highlight(code_text, lexers.find_lexer_class_by_name('python')(), formatters.find_formatter_class('html')() )

    model = {'code_text': highted_code}

    return render(request, 'html/crawler_app_view.html', model)


@login_required(login_url='/')
def crawler_edit(request, crawler_id):
    try:
        crawler_item = Crawler.objects.get(id=crawler_id)
    except:
        return crawler_list(request, msg="爬虫不存在")
    crawler = CrawlerSerializer(crawler_item, many=False)
    return render(request, 'html/crawler_edit.html', {
        'form': crawler.data
    })


@login_required(login_url='/')
@transaction.atomic
def crawler_edit_submit(request, **kwargs):
    model = handle_msg(kwargs)
    crawler_app_folder = "/etc/rhino/crawler_app"
    form = {}
    success = True
    if request.method == 'POST':
        crawler_id = request.POST.get('crawler_id')
        crawler = Crawler.objects.get(id=crawler_id)

        #project = request.POST.get('project')
        #project_id = request.POST.get('project_id')
        #project_name = request.POST.get('project_name')
        crawler_name = request.POST.get('crawler_name', None)
        crawler_app = request.FILES.get('crawler_app', None)
        clean_app = request.FILES.get('clean_app', None)
        clean_parameters = request.POST.get('clean_parameters', None)
        field_mapping = request.POST.get('field_mapping', '')
        field_mapping = field_mapping.replace('\n', '')
        field_mapping = field_mapping.replace('', '')
        nc = "off"
        try:
            nc = request.POST.get('need_clean', None)
        except Exception as e:
            need_clean = False
        if nc and nc == 'on':
            need_clean = True
        else:
            need_clean = False

        try:
            path = crawler_app_folder + '/' + crawler_id
            tasks = Task.objects.filter(crawler_id=crawler_id)
            if crawler_app: #如果用户重新上传了文件，则更新文件
                # 更新文件, 并更新cralwer类
                original_crawler_app = crawler.crawler_app
                crawler_app_file_name = crawler_app_folder + '/' + crawler_id + '/' + crawler_app.name
                crawler.crawler_app = crawler_app_file_name
                # 删除老的文件
                if original_crawler_app and len(original_crawler_app)\
                        and os.path.isfile(original_crawler_app) and os.path.exists(original_crawler_app):
                    os.remove(original_crawler_app)

                crawler_app_dest = open(os.path.join(path, crawler_app.name), 'wb+')
                for chunks in crawler_app.chunks():
                    crawler_app_dest.write(chunks)

                #同时修改所有的task
                for task in tasks:
                    task.crawler_app = crawler_app_file_name
                    task.save()

            if clean_app: #如果用户重新上传了清洗文件，则更新文件
                original_clean_app = crawler.clean_app
                # 删除老的文件
                if original_clean_app and len(original_clean_app) and os.path.isfile(original_clean_app)\
                        and os.path.exists(original_clean_app):
                    os.remove(original_clean_app)
                clean_app_file_name = crawler_app_folder + '/' + crawler_id + '/' + clean_app.name
                crawler.clean_app = clean_app_file_name

                clean_app_dest = open(os.path.join(path, clean_app.name), 'wb+')
                # 更新文件, 并更新cralwer类
                for chunks in clean_app.chunks():
                    clean_app_dest.write(chunks)

                # 同时修改所有的task
                for task in tasks:
                    task.clean_app = clean_app_file_name
                    task.save()

            # 同时修改所有的task
            for task in tasks:
                task.clean_parameters = clean_parameters
                task.save()

            crawler.fields_mapping = field_mapping
            crawler.crawler_name = crawler_name
            crawler.clean_parameters = clean_parameters
            crawler.update_time = time.time()
            crawler.save()
        except Exception as e:
            add_message(model, str(e), msg_type="error")
            success = False

        if success is True:
            add_message(model, "修改爬虫成功，新建任务才能生效。")
            return crawler_list(request, msg="修改爬虫成功，新建任务才能生效。")
        else:
            crawler_ser = CrawlerSerializer(crawler, many=False)
            return render(request, 'html/crawler_edit.html', {
                'form': crawler_ser.data
            })
    else:
        return crawler_list



@login_required(login_url='/')
def crawler_list(request, **kwargs):
    model = handle_msg(kwargs)
    project_ids = Project.objects.values_list('code', 'code', 'project_name')
    model['project_ids'] = project_ids
    return render(request, 'html/crawler_list.html', model)


@login_required(login_url='/')
@api_view(['POST'])
def crawler_list_api(request):
    search_keyword = request.POST.get('search_keyword', '')
    limit = request.POST.get('limit', '10')
    offset = request.POST.get('offset', '0')
    project_id = request.POST.get('project_id', '')
    crawlers = Crawler.objects.only('id', 'crawler_name', 'project_id', 'project_name', 'create_time', 'update_time',
                                    'crawler_app', 'clean_app').order_by('-update_time')
    searchQ = Q(crawler_name__contains=search_keyword)
    projectQ = Q(project_id=project_id)
    if len(search_keyword) > 0:
        crawlers = crawlers.filter(
            searchQ)
    if len(project_id) > 0:
        crawlers = crawlers.filter(projectQ)

    size = crawlers.count()
    if limit and limit == '-1':
        data = crawlers[int(offset):]
    else:
        data = crawlers[int(offset):int(offset) + int(limit)]
    crawler_ser = CrawlerSerializer(data, many=True)

    crawlers_obj = crawler_ser.data

    for crawler in crawlers_obj:
        if crawler['clean_method'] == 'common':
            processor = Processor.objects.get(id=crawler['processor_id'])
            crawler['deploy_target'] = processor.deploy_target
            validate_rules = ValidateRule.objects.filter(task_id=crawler['processor_id'])
            validate_rules_ser = ValidateRuleSerializer(validate_rules, many=True).data
            crawler['validate_rules'] = json.dumps(validate_rules_ser)

    return Response({"data": crawlers_obj, "size": size})

