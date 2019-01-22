from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
# Create your views here.

from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth import logout as django_logout
from django.contrib.auth import login as django_login
from django.contrib.auth.decorators import login_required
from rhino.util import file_util

def index(request):
    if request.user.is_authenticated():
        return overview(request)
    return redirect('login')


def login(request):

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                django_login(request, user)
                return redirect('index')
                # return overview(request)
            else:
                return render(request, 'html/index.html', {"form":
                    {
                        "username": username,
                        "password": password
                    },
                    "message":
                        {"error": "用户未激活！"}
                })
        else:
            return render(request, 'html/index.html', {"form": {
                "username": username,
                "password": password
            }, "message": {"error": "用户名或密码错误！"}})
    else:
        return render(request, 'html/index.html')


def logout(request):
    django_logout(request)
    return HttpResponseRedirect('/')


@login_required(login_url='/')
def file_download(request, file_name):
    return file_util.big_file_download(file_name)


def overview(request):
    return render(request, 'html/bigscreen_bk.html')

