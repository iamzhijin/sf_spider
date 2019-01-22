#! /user/bin/env python
# ——×—— coding:utf-8 ——×——
from django.shortcuts import render
from elasticsearch import Elasticsearch
from .models import webMonitor_task,webMonitor_resultNum
import datetime
import json
from rest_framework.decorators import api_view
import traceback
from rhino.settings import ELASTIC_SEARCH_SERVER,ELASTIC_SEARCH_PORT
# es地址
ELASTIC_SEARCH_ADDRESS = ELASTIC_SEARCH_SERVER+":"+ELASTIC_SEARCH_PORT

# 跳转
def go2manual_trigger_web_monitor(request):
    return render(request,'html/manual_trigger_web_monitor.html')


# 查询es 并且对比
@api_view(['POST'])
def manual_trigger_web_monitor(request):
    if request.method =='POST':
        # 查询es 然后比较出结果，并保存到mysql
        # 线上
        es = Elasticsearch([ELASTIC_SEARCH_ADDRESS])
        # 线下
        # es = Elasticsearch(['10.1.1.28:9200'])
        # # 查询es 获取裁判文书，失信被执行人，被执行人，曝光台，全量各source数据 返回dict
        es_result_dict = getES_search(es)
        print("es_result_dict")
        print(es_result_dict)


        # 查询 mysql 对应各个dataType 进行逐条对比
        webMonitorInfo_list = request.POST['webMonitorInfo_list']
        result_mysql_list = json.loads(webMonitorInfo_list)
        for item in result_mysql_list:
            web_name = item['web_name']
            web_num = item['web_num']
            print(web_name)
            print(web_num)
            data_type = item['data_type']
            # try:
            #     web_num = int(web_num)
            # except:
            #     continue
            compare_mysql2es(web_name, web_num, data_type, es_result_dict)
        content={
            "result":"完成"
        }
        return render(request,'html/manual_trigger_web_monitor.html',content)



def compare_mysql2es(web_name,web_num,data_type,es_result_dict):
    es_num = ""
    # 获取es对应数据
    if data_type=='裁判文书':
        key = verdict_DataType(web_name)
        print(key)
        try:
            for item in es_result_dict['judge_doc']:
                if key == item['key']:
                    es_num = item['doc_count']
                    break
        except:
            pass
            es_num ="-1"
    elif data_type =="失信被执行人" or data_type =="失信人":
        try:
            for item in es_result_dict['shixin_beizhixing']:
                if web_name == item['key']:
                    es_num = item['doc_count']
                    break
        except:
            pass
            es_num ="-1"
    elif data_type =="开庭公告":
        key = verdict_DataType(web_name)
        try:
            for item in es_result_dict['court_session_announcement']:
                if key == item['key']:
                    es_num = item['doc_count']
                    break
        except:
            pass
            es_num = "-1"
    elif data_type =="被执行人":
        try:
            for item in es_result_dict['executive_announcement']:
                if web_name == item['key']:
                    es_num = item['doc_count']
                    break
        except:
            pass
            es_num ="-1"
    else:
        try:
            for item in es_result_dict['exposure_desk']:
                if web_name == item['key']:
                    print(item)
                    es_num = item['doc_count']
                    break
        except:
            pass
            es_num ="-1"

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
        status="es无数据的"

    try:
        web_num = int(web_num)
        es_num = int(es_num)
        result_num = round(es_num / web_num, 2)
        es_num = str(es_num)
    except:
        status = "es无数据的"
    if web_name !="天津法院网-开庭公告":
        try:
            if isinstance(web_num,str):
                web_num = int(web_num)
            if web_num <0:
                status = "未爬取成功"
        except:
            status = "未爬取成功"



    if isinstance(result_num,float) and result_num <=0.9 and result_num>=0.0:
        status = "预警"
    if result_num and result_num >0.9:
        status = "ok"
    webMonitor_resultNum.objects.filter(web_name=web_name).update(es_num=es_num ,status=status)


# 查询es 获取裁判文书，失信被执行人，被执行人，曝光台，全量各source数据
def getES_search(es):

    result_dict={}
    tmp_dict = {
        "judge_doc":"local_doc",
        "shixin_beizhixing":"shixin_beizhixing_gaoyuan",
        "exposure_desk":"exposure_desk",
        "executive_announcement": "executive_announcement_gaoyuan",
    }

    for index,doc_type in tmp_dict.items():
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
    start_date = str(today)+"T00:00:00+08:00"
    end_date = str(end) + "T00:00:00+08:00"
    query_ktgg= """
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
    
    """%(start_date,end_date)
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
def verdict_DataType(web_name):
    try:
        region_web_name = web_name.split(r'-')[0]
        return region_web_name
    except:
        pass