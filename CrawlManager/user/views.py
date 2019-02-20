from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .form import RegistForm
from django.contrib.auth.models import User
import datetime
from django.core.mail import send_mail
from django.conf import settings

def regist_html(request):
    return render(request, 'user/regist.html')


def regist(request):
    '''regist an accont'''
    if request.method == 'POST':
        regist_form = RegistForm(request.POST)
        if regist_form.is_valid():
            data = regist_form.clean()
            username = data['username']
            password = data['password']
            email = data['email']
            is_superuser = 0
            is_staff = 0
            is_active = 0
            date_joined = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')           
            # 创建一个尚未激活的普通用户
            user = User.objects.create_user(
                username=username, 
                password=password, 
                email=email,
                is_superuser=is_superuser,
                is_staff=is_staff,
                is_active=is_active,
                date_joined=date_joined
            )
            send = send_regist_email(username, email)  # 发送激活邮件
            if send:
                return HttpResponse('success')          
            else:
                return 'fase'
        else:
            error_meg = regist_form.errors.as_json()
            return HttpResponse(error_meg)        
    return HttpResponse(regist_form)


def send_regist_email(username, email):
    '''send email to make acount active'''
    try:
        email_title = '帐号激活'
        email_msg = '%s 激活帐号完成注册流程' % username 
        receive_email = [email] 
        email_msg_html = '点击连接进行激活http://127.0.0.1:8000/crawlManager/user/active?username=%s' % username   
        send_mail(email_title, email_msg_html, settings.EMAIL_HOST_USER, receive_email, fail_silently=False)
        return True
    except Exception as e:
        print(e)
        return False 


def active_acount(request):
    pass


def login(request):
    pass


def logout(request):
    pass           
