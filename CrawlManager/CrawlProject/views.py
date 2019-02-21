from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .form import ProjectForm
from .models import Project
from CrawlManager.Util import Util
import json

util = Util()

def ManageProject(request):
    return render(request, 'CrawlProject/ProjectList.html')


def CreateProject(request):
    '''创建新的爬虫项目'''
    if request.method == "POST":
        project_form = ProjectForm(request.POST) 
        if project_form.is_valid():
            project_form_data = project_form.clean()
            insert_project = Project(
                project_name=project_form_data['project_name'],
                code=project_form_data['code'],
                describe=request.POST['describe'],               
            )
            insert_project.save()
            return JsonResponse(util.success_result())
        else:
            error_message = project_form.errors.as_text()  
            return JsonResponse(util.fail_result(data=error_message))
    else:
        return render(request, 'CrawlProject/CreateProject.html')
        # return JsonResponse(util.fail_result(code='002'))


def DeleteProject(request):
    '''根据id删除爬虫项目'''
    if request.method == "POST":
        project_id = request.POST['id']
        try:
            Project.objects.get(id=project_id).delete()   
            return JsonResponse(util.success_result())
        except Exception as e:    
            return JsonResponse(util.fail_result(code='001')) 
    else:
        return JsonResponse(util.fail_result(code='002'))             


def ProjectList(request):
    '''分页展示爬虫列表'''
    if request.method == "GET":
        offset = int(request.GET['offset'])
        limit = int(request.GET['limit'])           
        project_list = Project.objects.all().values()[offset : offset*limit+limit]
        for each_project in project_list:
            each_project['update_time'] = each_project['update_time'].strftime('%Y-%m-%d %H:%M:%S')
            each_project['create_time'] = each_project['create_time'].strftime('%Y-%m-%d %H:%M:%S')
        total_num = len(Project.objects.all())
        data = {
            "size": total_num,
            "data": list(project_list)
        }
        # return render(request, 'CrawlProject/ProjectList.html', context=data)
        return HttpResponse(json.dumps(data))
    else:
        return JsonResponse(util.fail_result(code='002')) 
        