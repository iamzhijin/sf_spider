from django.shortcuts import render
from .models import Code_AI
from rest_framework.decorators import api_view
from django.http import JsonResponse
import json
from rhino.util.general_response import ApiGeneralResponse
# 邮件
from django.core.mail import send_mail,BadHeaderError

@api_view(['POST'])
def Email_send(request):
    fro = 'automail@yscredit.com'
    if request.method=='POST':
        print(request.POST)
        title = request.POST.get('title','')
        body = request.POST.get('body', '')
        receiver = request.POST.getlist('receiver')
        print(title,receiver,body)
        if title and body and receiver:
            try:
                send_mail(title, body, fro, receiver, fail_silently=False )
            except BadHeaderError:
                return ApiGeneralResponse(code=False,msg='发送失败').get_response()

            return ApiGeneralResponse(code=True,msg='发送成功').get_response()
        else:
            return ApiGeneralResponse(code=False, msg='发送失败',data={'reason':"参数不对"}).get_response()



@api_view(['POST'])
def code_ai(request):
    try:
        name = request.POST['name']
        succeed = request.POST['succeed']
        result = request.POST['result']
        image_binary = request.POST['image_binary']
        print(name, succeed, result, image_binary)
        case_id = Code_AI(name=name, succeed=succeed, result=result, image_binary=image_binary)
        case_id.save()
        return JsonResponse({'code': '0000'})
    except:
        return JsonResponse({'code': '0001'})