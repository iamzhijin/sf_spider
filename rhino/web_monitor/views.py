from django.shortcuts import render
from .models import webMonitor_task,webMonitor_resultNum
from .serializer import webMonitor_resultNum_Serializers,webMonitor_taskSerializers
from rest_framework.response import Response
from rhino.util.general_response import ApiGeneralResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
import json,time,re
import requests
from lxml import etree
from celery.app import task
# from django.utils import timezone as datetime
import datetime
# Create your views here.
from django.db.models import F,Q
from elasticsearch import Elasticsearch
from rhino.settings import ELASTIC_SEARCH_SERVER,ELASTIC_SEARCH_PORT
from django.http import HttpResponseRedirect
# es地址
ELASTIC_SEARCH_ADDRESS = ELASTIC_SEARCH_SERVER+":"+ELASTIC_SEARCH_PORT
# 创建监控页面
def go2create_web_monitor_html(request):
    return render(request,'html/create_web_monitor.html')


# 跳转到网页监控页面
def show_web_monitor(request):
    return render(request,"html/show_web_monitor.html")

# 查询监控任务
@api_view(['POST'])
def web_monitor_list_api(request):
    if request.method == 'POST':
        limit = request.POST.get('limit')
        offset = request.POST.get('offset')
        print(request.POST)
        data_type = request.POST.get('data_type')
        search_keyword = request.POST.get('search_keyword')
        if data_type=='开庭公告':
            data_type_str = "开庭公告"
            webMonitor_taskList = webMonitor_task.objects.filter(data_type=data_type_str).order_by('-web_update_time').filter(web_name__contains=search_keyword)
            data=webMonitor_taskList
            size = webMonitor_taskList.count()
        elif data_type=='曝光台':
            data_type_list = ["开庭公告","裁判文书","失信被执行人","失信人","被执行人","法院公告","送达公告"]
            webMonitor_taskList = webMonitor_task.objects.exclude(data_type__in=data_type_list).order_by('-web_update_time').filter(web_name__contains=search_keyword)
            data=webMonitor_taskList
            size = webMonitor_taskList.count()
        elif data_type == '裁判文书':
            data_type_str = "裁判文书"
            webMonitor_taskList = webMonitor_task.objects.filter(data_type=data_type_str).order_by('-web_update_time').filter(web_name__contains=search_keyword)
            data=webMonitor_taskList
            size = webMonitor_taskList.count()
        elif data_type == '失信被执行':
            data_type_str1 = "失信被执行人"
            data_type_str2 = "失信人"
            webMonitor_taskList = webMonitor_task.objects.filter(Q(data_type=data_type_str1)|Q(data_type=data_type_str2)).order_by('-web_update_time').filter(web_name__contains=search_keyword)
            data=webMonitor_taskList
            size = webMonitor_taskList.count()
        elif data_type == '被执行人':
            data_type_str1="被执行人"
            webMonitor_taskList = webMonitor_task.objects.filter(Q(data_type=data_type_str1)).order_by('-web_update_time').filter(web_name__contains=search_keyword)
            data=webMonitor_taskList
            size = webMonitor_taskList.count()
        elif data_type == '法院公告':
            data_type_str1 = "法院公告"
            data_type_str2 = "送达公告"
            webMonitor_taskList = webMonitor_task.objects.filter(Q(data_type=data_type_str1) | Q(data_type=data_type_str2)).order_by('-web_update_time').filter(web_name__contains=search_keyword)
            data = webMonitor_taskList
            size = webMonitor_taskList.count()
        else:
            webMonitor_taskList = webMonitor_task.objects.order_by('-web_update_time').filter(web_name__contains=search_keyword)
            size = webMonitor_taskList.count()
            if limit and limit == '-1':
                data = webMonitor_taskList[int(offset):]
            else:
                data = webMonitor_taskList[int(offset):int(offset) + int(limit)]
        crawler_ser = webMonitor_taskSerializers(data, many=True)
        return Response({"data": crawler_ser.data, "size": size})

# 测试
@api_view(['POST'])
def test_web_monitor_task(request):
    if request.method == "POST":
        print(request.POST)
        web_name = request.POST['web_name'].strip()
        web_site = request.POST['web_site'].strip()
        request_function = request.POST['request_function'].strip()
        request_body = request.POST['request_body'].strip()
        response_type = request.POST['response_type'].strip()
        xpath_str = request.POST['xpath_str'].strip()
        re_str = request.POST['re_str'].strip()
        keyword = request.POST['keyword'].strip()
        per_num = request.POST['per_num'].strip()
        if per_num:
            per_num = int(per_num)

        url = web_site
        #判断请求方式
        if request_function=='GET':
            # get方法获取html
            html =request_GET(url)
            # 获取数据量
            num = handle_html(html, xpath_str, re_str)
        else:
            # 对body做处理
            if request_body:
                request_body = handler_body(web_name,request_body)
            html = request_POST(url, request_body)
            # 判断是html还是interface
            if response_type=='HTML':
                num = handle_html(html, xpath_str, re_str)
            else:
                #接口
                num = handle_interface(html, keyword)

        try:
            if per_num :
                per_num = int(per_num)
                if per_num>0:

                    num = int(num) * per_num
        except:
            num = "每页数量：{}".format(per_num)+"爬取数量：{}".format(num)
        tmp_dict = {
            "num":num
        }
        print(tmp_dict)
        return JsonResponse(tmp_dict)




# 处理请求主体
def handler_body(web_name,request_body):
    tmp_dict = {}
    if '&' in request_body:
        request_body = request_body.split(r'&')
        for item in request_body:
            print(item)
            key = item.split(r'=')[0]
            value = item.split(r'=')[1]
            tmp_dict[key] = value
    else:
        key = request_body.split(r'=')[0]
        value = request_body.split(r'=')[1]
        tmp_dict[key] = value
    # 对时间做识别和处理
    if web_name !="浙江法院公开网-裁判文书":
        format_str_list = ["%Y-%m-%d", "%Y%m%d", "%Y/%m/%d"]
        tmp_dict = handler_date_string(tmp_dict, format_str_list)

    # dict转换成A=123&B=123
    tmp_str=""
    for k,v in tmp_dict.items():
        tmp = str(k)+"="+str(v)+"&"
        tmp_str+=tmp
    tmp_str = tmp_str[:-1]

    return tmp_dict,tmp_str


# GET请求
def request_GET(url):
    html = ""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }
    time = 4
    while time > 0:
        try:
            res = requests.get(url, headers=headers, timeout=25)
            res.encoding = res.apparent_encoding
            html = res.text
            break
        except:
            time -= 1
    return html

# POST请求
def request_POST(url,request_body):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }
    time = 4
    html=""
    while time > 0:
        try:
            res = requests.post(url, headers=headers,data=request_body ,timeout=25)
            res.encoding = res.apparent_encoding
            html = res.text
            break
        except:
            time -= 1
    return html

# html处理
def handle_html(html,xpath_str,re_str):
    selector = etree.HTML(html)
    try:
        if xpath_str and not re_str:
            num = selector.xpath(xpath_str)[0]
        elif xpath_str and not re_str:
            line = selector.xpath(xpath_str)[0]
            num = re.findall(re_str, line)[0]
        else:
            num = re.findall(re_str, html)[0]
    except:
        num=-1
    return num

# interface处理
def handle_interface(html,keyword):
    num=""
    try:
        html = json.loads(html)
        html = eval(html)
    except:
        pass
    if isinstance(html,list):
        for item in html:
            if keyword in item:
                num = item[keyword]
    else:
        num = html[keyword]
    return num








# 创建监控任务
@api_view(['POST'])
def create_web_monitor_task(request):
    if request.method=='POST':
        web_name= request.POST['web_name']
        web_site= request.POST['web_site']
        request_function= request.POST['request_function']
        request_body = request.POST['request_body']
        xpath_str = request.POST['xpath_str']
        per_num= request.POST['per_num']
        response_type = request.POST['response_type']
        re_str = request.POST['re_str']
        keyword = request.POST['keyword']
        # 判断类型datatype和region_web_name
        region_web_name,dataType = verdict_DataType(web_name)
        w = webMonitor_task()

        w.web_name=web_name.strip()
        w.region_web_name = region_web_name.strip()
        w.data_type=dataType.strip()
        w.web_site = web_site.strip()
        w.request_function = request_function.strip()
        w.request_body = request_body.strip()
        w.xpath_str = xpath_str.strip()
        w.re_str = re_str.strip()
        w.response_type = response_type.strip()
        w.keyword = keyword.strip()
        if per_num :
            w.per_num = per_num
        else:
            w.per_num = -1
        w.save()


    return render(request,"html/show_web_monitor.html")

# 删除监控任务
@api_view(['POST'])
def delete_web_monitor(request):
    if request.method == 'POST':

        webMonitorInfo_list = request.POST['webMonitorInfo_list']
        webMonitorInfo_list = json.loads(webMonitorInfo_list)
        for item in webMonitorInfo_list:
            web_name = item['web_name']
            w = webMonitor_task.objects.filter(pk=web_name)
            w.delete()
        return Response({"data":1})


# 执行监控任务
@api_view(['POST'])
def run_web_monitor_task(request):
    if request.method == 'POST':
        print(request.POST)
        webMonitorInfo_list = request.POST['webMonitorInfo_list']
        webMonitorInfo_list = json.loads(webMonitorInfo_list)
        print(webMonitorInfo_list)
        today = str(datetime.date.today())
        # es
        es = Elasticsearch([ELASTIC_SEARCH_ADDRESS])
        es_result_dict = getES_search(es)
        print("es_result_dict")
        print(es_result_dict)
        for item in webMonitorInfo_list:

            web_name = item['web_name']
            print(web_name)
            data_type = item['data_type']
            web_site = item['web_site']
            request_function = item['request_function']
            request_body = item['request_body']
            response_type = item['response_type']
            xpath_str = item['xpath_str']
            re_str = item['re_str']
            keyword = item['keyword']
            per_num = item['per_num']
            # 爬取
            tmp_dict = do_monitor(web_name, web_site, request_function, request_body, response_type, xpath_str, re_str, keyword,
                   per_num)
            num = tmp_dict['num']

            # 对比
            es_num, status = compare_mysql2es(web_name, num, data_type, es_result_dict)
           # save num
            w = webMonitor_resultNum()
            w.web_name=web_name
            w.web_num=num
            w.web_date_start=today
            w.data_type=data_type
            w.es_num = es_num
            w.status = status
            w.save()
            print("爬取数据量：{}".format(num))

        return render(request,'html/results_web_monitor.html')
# 对比
# def manual_trigger_web_monitor(web_name,web_num,data_type,es_result_dict):
#         # 查询es 然后比较出结果，并保存到mysql
#         # # 查询es 获取裁判文书，失信被执行人，被执行人，曝光台，全量各source数据 返回dict
#
#
#         es_num, status = compare_mysql2es(web_name, web_num, data_type, es_result_dict)
#         return es_num, status

def do_monitor(web_name,web_site,request_function,request_body,response_type,xpath_str,re_str,keyword,per_num):
    num=-1
    if per_num:
        per_num = int(per_num)

    url = web_site
    try:
        # 判断请求方式
        if request_function == 'GET':
            # get方法获取html
            html = request_GET(url)
            # 获取数据量
            num = handle_html(html, xpath_str, re_str)
        else:
            # 对body做处理
            if request_body :
                request_body,request_str = handler_body(web_name,request_body)
                webMonitor_task.objects.filter(web_name=web_name).update(request_body=request_str)

                print("request_body")
                print(request_body)
            res = request_POST(url, request_body)
            # 判断是html还是interface
            if response_type == 'HTML':
                num = handle_html(res, xpath_str, re_str)
            else:
                # 接口
                num = handle_interface(res, keyword)
    except:
        num=-1
    if per_num:
        per_num = int(per_num)
        if per_num > 0:
            try:
                num = int(num) * per_num
                if num <0:
                    num=-1
            except:
                pass

    tmp_dict = {
        "num": str(num)
    }
    return tmp_dict




# 查询结果列表页
@api_view(['POST'])
def results_web_monitor_list_api(request):
    if request.method == 'POST':
        print(request.POST)
        # limit = request.POST.get('limit')
        # offset = request.POST.get('offset')
        limit ="200"
        offset = "0"
        data_type = request.POST.get('data_type')
        search_keyword = request.POST.get('search_keyword')
        result_status = request.POST.get('result_status')

        if data_type=='开庭公告':
            data_type_str = "开庭公告"
            webMonitor_taskList = webMonitor_resultNum.objects.filter(data_type=data_type_str).order_by('-web_date_start').filter(web_name__contains=search_keyword).filter(status__contains=result_status)
            data=webMonitor_taskList
            size = webMonitor_taskList.count()
        elif data_type=='曝光台':
            data_type_list = ["开庭公告","裁判文书","失信被执行人","失信人","被执行人","法院公告","送达公告"]
            webMonitor_taskList = webMonitor_resultNum.objects.exclude(data_type__in=data_type_list).order_by('-web_date_start').filter(web_name__contains=search_keyword).filter(status__contains=result_status)
            data=webMonitor_taskList
            size = webMonitor_taskList.count()
        elif data_type == '裁判文书':
            data_type_str = "裁判文书"
            webMonitor_taskList = webMonitor_resultNum.objects.filter(data_type=data_type_str).order_by('-web_date_start').filter(web_name__contains=search_keyword).filter(status__contains=result_status)
            data=webMonitor_taskList
            size = webMonitor_taskList.count()
        elif data_type == '失信被执行':
            data_type_str1 = "失信被执行人"
            data_type_str2 = "失信人"
            webMonitor_taskList = webMonitor_resultNum.objects.filter(Q(data_type=data_type_str1)|Q(data_type=data_type_str2)).order_by('-web_date_start').filter(web_name__contains=search_keyword).filter(status__contains=result_status)
            data=webMonitor_taskList
            size = webMonitor_taskList.count()
        elif data_type == '被执行人':
            data_type_str1="被执行人"
            webMonitor_taskList = webMonitor_resultNum.objects.filter(Q(data_type=data_type_str1)).order_by('-web_date_start').filter(web_name__contains=search_keyword).filter(status__contains=result_status)
            data=webMonitor_taskList
            size = webMonitor_taskList.count()
        elif data_type == '法院公告':
            data_type_str1 = "法院公告"
            data_type_str2 = "送达公告"
            webMonitor_taskList = webMonitor_resultNum.objects.filter(Q(data_type=data_type_str1) | Q(data_type=data_type_str2)).order_by('-web_date_start').filter(web_name__contains=search_keyword).filter(status__contains=result_status)
            data = webMonitor_taskList
            size = webMonitor_taskList.count()
        else:
            webMonitor_taskList = webMonitor_resultNum.objects.order_by('-web_date_start').filter(
                web_name__contains=search_keyword).filter(status__contains=result_status)
            size = webMonitor_taskList.count()
            # data = webMonitor_taskList
            if limit and limit == '-1':
                data = webMonitor_taskList[int(offset):]
            else:
                data = webMonitor_taskList[int(offset):int(offset) + int(limit)]
        crawler_ser = webMonitor_resultNum_Serializers(data, many=True)
        return Response({"data": crawler_ser.data, "size": size})


# 跳转到result_web_monitor.html
def results_web_monitor(request):
    return render(request,'html/results_web_monitor.html')


# 删除爬去结果
@api_view(['POST'])
def delete_results_web_monitor(request):
    if request.method == 'POST':
        results_webMonitorInfo_list = request.POST['results_webMonitorInfo_list']
        results_webMonitorInfo_list = json.loads(results_webMonitorInfo_list)

        for item in results_webMonitorInfo_list:
            web_name = item['web_name']
            w = webMonitor_resultNum.objects.filter(pk=web_name)
            w.delete()
        return Response({"data": 1})
# 存数据
def insert2model(web_name,num):
    w = webMonitor_resultNum()
    w.web_name = web_name
    w.webMonitor_result = num


# 判断类型
def verdict_DataType(web_name):
    try:
        region_web_name = web_name.split(r'-')[0]
        dataType = web_name.split(r'-')[-1]
        return region_web_name,dataType
    except:
        pass

# 把str转换成date
def string_toDatetime(date_str, format_str):
    return datetime.datetime.strptime(date_str, format_str)

# 转换时间
def transform_date(v,format_str_list):
    for format_str in format_str_list:
        try:
            date_str = string_toDatetime(v, format_str)
            today_str = datetime.datetime.now().strftime(format_str)
            today_str = string_toDatetime(today_str, format_str)
            if today_str>=date_str:
                date_str=today_str
            elif today_str<date_str:
                date_str = today_str + datetime.timedelta(weeks=480)


            date_str = date_str.strftime(format_str)
            date_str = str(date_str)
            return date_str
        except:
            continue

# 将今天日期赋值
def handler_date_string(tmp_dict,format_str_list):
    for k, v in tmp_dict.items():
        try:
            a = transform_date(v, format_str_list)
            if a:
                tmp_dict[k]=a
        except:
            pass
    return  tmp_dict


# 比较
def compare_mysql2es(web_name, web_num, data_type, es_result_dict):
    es_num = ""
    # 获取es对应数据
    if data_type == '裁判文书':
        key = verdict_DataType2(web_name)
        print(key)
        try:
            for item in es_result_dict['judge_doc']:
                if key == item['key']:
                    es_num = item['doc_count']
                    break
        except:
            pass
            es_num = "-1"
    elif data_type == "失信被执行人" or data_type == "失信人":
        try:
            for item in es_result_dict['shixin_beizhixing']:
                if web_name == item['key']:
                    es_num = item['doc_count']
                    break
        except:
            pass
            es_num = "-1"
    elif data_type == "开庭公告":
        key = verdict_DataType2(web_name)
        try:
            for item in es_result_dict['court_session_announcement']:
                if key == item['key']:
                    es_num = item['doc_count']
                    break
        except:
            pass
            es_num = "-1"
    elif data_type == "被执行人":
        try:
            for item in es_result_dict['executive_announcement']:
                if web_name == item['key']:
                    es_num = item['doc_count']
                    break
        except:
            pass
            es_num = "-1"
    else:
        try:
            for item in es_result_dict['exposure_desk']:
                if web_name == item['key']:
                    print(item)
                    es_num = item['doc_count']
                    break
        except:
            pass
            es_num = "-1"

    status = ""
    result_num = ""
    # 对比数据
    print("=========")
    print(web_name)
    print("es:")
    print(es_num)
    print("web:")
    print(web_num)
    print("=========")
    if not es_num and web_num:
        status = "es无数据的"

    try:
        web_num = int(web_num)
        es_num = int(es_num)
        result_num = round(es_num / web_num, 2)
        es_num = str(es_num)
    except:
        status = "es无数据的"
    if web_name != "天津法院网-开庭公告":
        try:
            if isinstance(web_num, str):
                web_num = int(web_num)
            if web_num < 0:
                status = "未爬取成功"
        except:
            status = "未爬取成功"

    if isinstance(result_num, float) and result_num <= 0.9 and result_num >= 0.0:
        status = "预警"
    if result_num and result_num > 0.9:
        status = "ok"
    # webMonitor_resultNum.objects.filter(web_name=web_name).update(es_num=es_num, status=status)
    return es_num,status

# 查询es 获取裁判文书，失信被执行人，被执行人，曝光台，全量各source数据
def getES_search(es):
    result_dict = {}
    tmp_dict = {
        "judge_doc": "local_doc",
        "shixin_beizhixing": "shixin_beizhixing_gaoyuan",
        "exposure_desk": "exposure_desk",
        "executive_announcement": "executive_announcement_gaoyuan",
    }

    for index, doc_type in tmp_dict.items():
        query = """
            {
                  "size": 0,
                  "query": {
                    "bool": {
                      "must": [
                        {
                          "query_string": {
                            "query": "*",
                            "analyze_wildcard": true
                          }
                        }
                      ],
                      "must_not": []
                    }
                  },
                  "aggs": {
                    "2": {
                      "terms": {
                        "field": "source",
                        "size": 500,
                        "order": {
                          "_count": "desc"
                        }
                      }
                    }
                  }
                }
            """

        es_result = es.search(
            index=index,
            doc_type=doc_type,
            scroll='5m',
            timeout='5m',
            body=query,
        )

        # total = es_result['hits']['total']
        res_list = es_result['aggregations']['2']['buckets']
        result_dict[index] = res_list
    # 开庭公告
    today = datetime.date.today()
    end = today + datetime.timedelta(weeks=480)
    start_date = str(today) + "T00:00:00+08:00"
    end_date = str(end) + "T00:00:00+08:00"
    query_ktgg = """
    {
          "size": 0,
          "query": {
            "bool": {
              "must": [
                {
                  "query_string": {
                    "analyze_wildcard": true,
                    "query": "*"
                  }
                },
                {
                  "range": {
                    "court_date": {
                      "gte": "%s",
                      "lte": "%s"
                    }
                  }
                }
              ],
              "must_not": []
            }
          },
          "_source": {
            "excludes": []
          },
          "aggs": {
            "4": {
              "terms": {
                "field": "source",
                "size": 500,
                "order": {
                  "_count": "desc"
                }
              }
            }
          }
        }

    """ % (start_date, end_date)
    es_result_ktgg = es.search(
        index="court_session_announcement",
        doc_type="court_session_announcement",
        scroll='5m',
        timeout='5m',
        body=query_ktgg,
    )
    res_list_ktgg = es_result_ktgg["aggregations"]["4"]["buckets"]
    result_dict["court_session_announcement"] = res_list_ktgg

    return result_dict


# 判断类型
def verdict_DataType2(web_name):
    try:
        region_web_name = web_name.split(r'-')[0]
        return region_web_name
    except:
        pass

