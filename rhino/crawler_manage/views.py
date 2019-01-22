from django.shortcuts import render
from django.http import HttpResponse
from .models import Project
from django.shortcuts import get_object_or_404

# Create your views here.


def list_projects(request):
    projects = Project.objects.order_by('-update_time')[:10]
    context = {
        'html': projects
    }
    return render(request, 'html/projects_list.html', context)



def show_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'html/project_detail.html',
                  {'project': project})


def get_valid_rules(request, task_id):
    pass
