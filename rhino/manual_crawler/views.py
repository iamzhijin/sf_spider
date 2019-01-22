from django.shortcuts import render
from .models import manual_crawler_info
from rest_framework.decorators import api_view
from .serializer import manualCrawlerSerialzers
from rest_framework.response import Response
from threading import Thread
from urllib import parse
import requests,time,datetime
import threading
import re
import threadpool
import json
from rhino.settings import MANUAL_CRAWLER_URL,MANUAL_CRAWLER_USERNAME,MANUAL_CRAWLER_PASSWORD
# 测试线程池
pool = threadpool.ThreadPool(10)


def manual_crawler_show(request):

    # m = manual_crawler_info.objects.all()
    return render(request,'html/manual_crawler_show.html')

# 提交
#  #　id  用于给请求拿号
#     #　crawler_type 裁判文书，失信被执行，被执行人
#     crawler_type = models.CharField(max_length=10)
#     # type 1:企业名　2:人名
#     type = models.IntegerField()
#     # name
#     ent_person_name = models.CharField(max_length=100)
#     # create_time 创建时间
#     create_time = models.DateTimeField(auto_now=True)
#     # flag_status 0是没有完成　1是正在爬去　2　是完成了
#     flag_status = models.IntegerField()

# 创建任务
@api_view(['POST','GET'])
def submit_crawler(request):
    if request.method == 'POST':

        POST = request.POST
        print(POST)
        # 爬虫类型：裁判文书，被执行人，失信被执行人
        crawler_type_list = request.POST.getlist('crawler_type')
        # １是企业　２是人名
        type = request.POST['type']
        # 企业名　或者人名
        ent_person_name = request.POST['ent_person_name']
        ent_person_name_list = re.split(r'\r\n', ent_person_name)

        # 未进行
        flag_status = 0
        for crawler_type in crawler_type_list:
            for ent_person_name in ent_person_name_list:
                m = manual_crawler_info(crawler_type = crawler_type,type = type,ent_person_name = ent_person_name,flag_status = flag_status)
                m.save()
        msg_submit = {"code":"提交成功"}

        # # 批量触发,今天提交的
        # flag_status0crawlers_today_list = manual_crawler_info.objects.filter(flag_status=0).filter(create_time__gte=datetime.date.today())
        # print(flag_status0crawlers_today_list)
        # params_list = []
        # for crawler in flag_status0crawlers_today_list:
        #     id = crawler.id
        #     crawler_type = crawler.crawler_type
        #     type = crawler.type
        #     ent_person_name = crawler.ent_person_name
        #     print(crawler_type,type,ent_person_name)
        #     # 组合参数
        #     tmp_list =[]
        #     tmp_list.append(id)
        #     tmp_list.append(crawler_type)
        #     tmp_list.append(type)
        #     tmp_list.append(ent_person_name)
        #     params_list.append((tmp_list,None))
        #
        # requests2 = threadpool.makeRequests(do_manual_crawler,params_list)
        # [pool.putRequest(req)  for req in requests2]


        return render(request,'html/manual_crawler_show.html',msg_submit)
# 查询任务
@api_view(['POST'])
def crawler_list_api(request):
    if request.method == 'POST':
        print("requestPOST:")
        print(request.POST)
        limit = request.POST['limit']
        offset = request.POST['offset']
        status = request.POST['status']
        search_keyword = request.POST['search_keyword']
        tmp_dict ={
            "待启动": 0,
            "正在爬取": 1,
            "成功":2,
            "失败": 3,
            "0002": 4,
        }
        try:
            status = tmp_dict[status]
        except:
            status=""
        if not status and status!=0 :
            crawerInfoList = manual_crawler_info.objects.order_by('-id').filter(ent_person_name__contains=search_keyword)
        else:
            crawerInfoList = manual_crawler_info.objects.filter(flag_status=status).order_by('-id').filter(ent_person_name__contains=search_keyword)
        # else:
        #     crawerInfoList = manual_crawler_info.objects.filter(flag_status__range=[1, 2]).order_by('-id')
        size = crawerInfoList.count()
        data = crawerInfoList
        crawler_ser = manualCrawlerSerialzers(data, many=True)
        return Response({"data": crawler_ser.data, "size": size})

# 删除按钮
@api_view(['POST'])
def delete_manual_crawler(request):
    if request.method=='POST':
        a = request.POST
        tmp_list = a['crawlerInfo_list']
        tmp_list = json.loads(tmp_list)
        tmp_id_list=[]
        for tmp in tmp_list:
            id = tmp['id']
            tmp_id_list.append(id)
        print(tmp_id_list)
        c = manual_crawler_info.objects.filter(id__in=tmp_id_list)
        c.delete()
        # return 1
        # return (request,'html/manual_crawler_show.html')
        return Response(data={'code':0000})

# RUN按钮 ：触发
@api_view(['POST'])
def run_manual_crawler(request):

    a = request.POST
    crwawler_list = request.POST['crwawler_list']
    crwawler_list = json.loads(crwawler_list)
    for item in crwawler_list:
        print(item)
        id = item['id']
        crawler_type = item['crawler_type']
        type = item['type']
        ent_person_name = item['ent_person_name']
        do_manual_crawler(id, crawler_type, type, ent_person_name)
    return Response(data={'code':0000})

# 爬虫接口
def do_manual_crawler(id,crawler_type,type,ent_person_name):
    # 0 ：初始状态　１：　正在爬取　　２：完成　３　失败
    manual_crawler_info.objects.filter(pk=id).update(flag_status=1)
    original_url = MANUAL_CRAWLER_URL
    crawler_type_dict = {
        "judge_doc":"ws_web",
        "executive_announcement":"bzxr",
        "shixin_beizhixing":"sxbzxr"
    }
    crawler_type = crawler_type_dict[crawler_type]
    part_url = original_url+crawler_type+"?"

    formatted_data = {
        "name": ent_person_name,
        "type": type,
        "username": MANUAL_CRAWLER_USERNAME,
        "password": MANUAL_CRAWLER_PASSWORD
    }
    params = parse.urlencode(formatted_data)
    url = part_url + params
    try:
        res = requests.get(url, timeout=100).text
        print(res)
        res = json.loads(res)
        if res['code']=='0000':
            manual_crawler_info.objects.filter(pk=id).update(flag_status=2)
        elif res['code']=='0002':
            manual_crawler_info.objects.filter(pk=id).update(flag_status=4)
    except :
        print("失败。。。")
        manual_crawler_info.objects.filter(pk=id).update(flag_status=3)
# class crawler_thread(threading.Thread):
#     def __init__(self,id,crawler_type_str,type,ent_person_name):
#         threading.Thread.__init__(self)
#         # id, crawler_type_str, type, ent_person_name
#         self.id = id
#         self.crawler_type_str = crawler_type_str
#         self.type = type
#         self.ent_person_name = ent_person_name
#
#     def run(self):
#         do_manual_crawler(self.id,self.crawler_type_str,self.type,self.ent_person_name)
#         # print(1)


