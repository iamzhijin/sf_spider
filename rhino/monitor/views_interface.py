#!/usr/bin/env python
# -*- coding:utf-8 -*-
from elasticsearch import Elasticsearch
from django.http import *
from rest_framework.response import Response
from .models import *
from rest_framework.decorators import api_view
import time,requests,traceback
from requests.adapters import HTTPAdapter
from rest_framework import serializers
from rhino.util.general_response import ApiGeneralResponse
import json,pymysql,configparser
from django.views.decorators.csrf import csrf_exempt
from rhino.settings import MYSQL_HOST,MYSQL_DB,MYSQL_USER,MYSQL_PASSWORD,ELASTIC_SEARCH_SERVER,ELASTIC_SEARCH_PORT
import datetime
from  web_monitor.models import webMonitor_resultNum
# mysql
# 连接mysql
conn = pymysql.connect(host=MYSQL_HOST, db=MYSQL_DB, port=3306, user=MYSQL_USER, password=MYSQL_PASSWORD, charset='utf8',
                           use_unicode=True)
cursor = conn.cursor()
# ES配置
# 线上
es_address = ELASTIC_SEARCH_SERVER + ":" +ELASTIC_SEARCH_PORT
es = Elasticsearch([es_address])



#　预警接口
@csrf_exempt
@api_view(['GET'])
def alert(request):
    if request.method =='GET':
        items_list = []
        # 查看mysql(网站上更新值)
        mysql_count_dayadd = getmysql_cpws()
        # webMOnitor 模型类
        webMonitor_result_list = webMonitor_resultNum.objects.filter(status="预警")
        count = 2
        for result in webMonitor_result_list:
            name = result.web_name
            tmp_dict={
                "id":count,
                "message":name
            }
            items_list.append(tmp_dict)
            count+=1
        # es中值
        ES_count = getES_cpws(es)
        # 计算比例
        try:
            percent = int(ES_count) / int(mysql_count_dayadd)
            if percent < 0.9:
                items_list.append({"id": 1, "message": "裁判文书更新缺失超10%"})
        except:
            items_list.append({"id":1,"message": "裁判文书网数据没有爬取到，请人工纠错"})


        tmp_dict =     {
           "items": items_list
        }
        return ApiGeneralResponse(code=True,msg="接口调用成功",data=tmp_dict).get_response()

# 走势图
@api_view(['POST'])
@csrf_exempt
def stat_history(request):
    if request.method == 'POST':
        type = request.POST['type']
        day = request.POST['duration']

        try:
            isinstance(int(day),int)
            day = int(day)-1
        except Exception:
            return ApiGeneralResponse(code=False,msg="duration必须为整数").get_response()
        if day < 0 or day == 0:
            return ApiGeneralResponse(code=False, msg="duration不能小于等于1").get_response()
        if type in ['ktgg','cpws','sxbzxr','bzxr','bgt','fygg']:
            tmp_dict = getES_ParamsAndName(type)
            name = tmp_dict["name"]
            index = tmp_dict['index']
            doc_type = tmp_dict['doc_type']
            today = str(datetime.date.today())+"T23:59:59+08:00"
            day15before = str(datetime.date.today() + datetime.timedelta(days=-int(day)))+"T00:00:00+08:00"
            # 开庭公告是create_time
            query_time_str = "update_time"
            if  type=='fygg':
                query_time_str = "create_time"
            elif type=='ktgg':
                query_time_str = "RS_CREATE_TIME"
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
                        },
                        {
                          "range": {
                            "%s": {
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
                    "2": {
                      "date_histogram": {
                        "field": "%s",
                        "interval": "1d",
                        "time_zone": "Asia/Shanghai",
                        "min_doc_count": 1
                      }
                    }
                  }
                }
             """ % (query_time_str,day15before, today,query_time_str)
            es_result = getES_search(query,index,doc_type)
            res_list = es_result['aggregations']['2']['buckets']

            # data_items
            data_items = []
            for res in res_list:
                date_dict = {}
                date_str = res['key_as_string'][:10]
                doc_count = res['doc_count']
                date_dict['date'] = date_str
                date_dict['count'] = int(doc_count)
                data_items.append(date_dict)

            # data
            data_dict = {
                "type": type,
                "name": name,
                "data_items": data_items
            }
            # statuses
            return ApiGeneralResponse(code=True,msg="返回数据成功",data=data_dict).get_response()
        else:
            return ApiGeneralResponse(code=False, msg="type错误").get_response()

# 数据量统计

@api_view(['POST'])
@csrf_exempt
def stat_overview(request):
    if request.method == 'POST':
        type = request.POST['type']
        date_str = request.POST['date']
        # 日期
        today = datetime.date.today()

        # 对日期的处理
        try:
            t = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            t_1 = t + datetime.timedelta(days=+1)
            date_str1 = str(t)+"T00:00:00+08:00"
            date_str2 = str(t_1)+"T00:00:00+08:00"
            if t>today:
                return ApiGeneralResponse(code=False, msg="date不能大于今天").get_response()
        except Exception:
            return ApiGeneralResponse(code=False,msg="date不对").get_response()
        if type in ['ktgg','cpws','sxbzxr','bzxr','bgt','fygg']:
            tmp_dict = getES_ParamsAndName(type)
            name = tmp_dict["name"]
            index = tmp_dict['index']
            doc_type = tmp_dict['doc_type']
            #=======total=============
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
                  "_source": {
                    "excludes": []
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
            es_result = getES_search(query, index, doc_type)
            total = es_result['hits']['total']
            total_list = es_result['aggregations']['2']['buckets']
            total_source_res_dict={}
            for source_total in total_list:
                source = source_total['key']
                doc_count_total = source_total['doc_count']
                total_source_res_dict[source]={}
                total_source_res_dict[source]['source']=source
                total_source_res_dict[source]['total']=int(doc_count_total)
                total_source_res_dict[source]['day_update'] = 0
            #======update===============
            # 开庭公告是create_time
            query_time_str = "update_time"
            if   type=='fygg':
                query_time_str = "create_time"
            elif type=='ktgg' :
                query_time_str = "RS_CREATE_TIME"

            query_update_common = """
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
                    },
                    {
                      "range": {
                        "%s": {
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
                 """ %(query_time_str,date_str1, date_str2)
            es_result = getES_search(query_update_common,index, doc_type)
            # 当天更新总量
            total_update = es_result['hits']['total']
            # 当天更新source列表和各数量
            update_list = es_result['aggregations']['2']['buckets']
            for update in update_list:
                source = update['key']
                doc_count_update = update['doc_count']
                total_source_res_dict[source]['day_update']=int(doc_count_update)
            #=======source_stat==============
            source_stat=[]
            for source in total_source_res_dict.keys():
                source_stat.append(total_source_res_dict[source])
            # if type=='fygg':
            #     source_stat.append({
            #         "source":"法院公告",
            #         "day_update":int(total_update),
            #         "total": int(total)
            #     })
            #=====================
            tmp_res = {
               "type": type,
               "name": name,
               "date": date_str,
               "data_items": {
                  "total": int(total),
                  "day_update": int(total_update),# 当天更新多少条
                  "source_stat": source_stat
               }

        }
            return ApiGeneralResponse(code=True,msg="返回数据成功",data=tmp_res).get_response()
        else:
            #type不对的情况
            return ApiGeneralResponse(code=False,msg="type错误").get_response()

@api_view(['POST'])
def daily_increase_ratio_api(request):
    if request.method=='POST':
        duration = request.POST['duration']
        duration = int(duration)
        total2day_increase_ratio_list = []


        # 遍历时间 对每天进行数据搜索 看是否有数据
        for i in range(1, duration + 1):
            date_str = str(datetime.date.today() + datetime.timedelta(days=-i))
            try:
                ratio = daily_increase_ratio.objects.get(as_of_day=date_str).value
                tmp_dict = {}
                tmp_dict['date']=date_str
                tmp_dict['ratio']=ratio
                total2day_increase_ratio_list.append(tmp_dict)
            except:
                # 如果没有则查询那一天的数据
                total2day_increase_ratio_list.append(calculate_ratio(date_str))

        return ApiGeneralResponse(code=True,msg="接口返回成功",data=total2day_increase_ratio_list).get_response()


 #######方法区###########

def getES_ParamsAndName(type):
    tmp_dict = {
        "ktgg":{
            "name":"开庭公告",
            "index":"court_session_announcement",
            "doc_type":"court_session_announcement"
        },
        "cpws": {
            "name": "裁判文书",
            "index": "judge_doc",
            "doc_type": "total_doc"
        },
        "sxbzxr": {
            "name": "失信被执行人",
            "index": "shixin_beizhixing",
            "doc_type": "shixin_beizhixing_total"
        },
        "bzxr": {
            "name": "被执行人",
            "index": "executive_announcement",
            "doc_type": "executive_announcement_total"
        },
        "bgt": {
            "name": "曝光台",
            "index": "exposure_desk",
            "doc_type": "exposure_desk"
        },
        "fygg": {
            "name": "法院公告",
            "index": "court_announcement",
            "doc_type": "court_announcement"
        }
    }
    return tmp_dict[type]

# 查询es
def getES_search(query,index,doc_type):
    es_result = es.search(
        index=index,
        doc_type=doc_type,
        scroll='5m',
        timeout='1m',
        body=query,
    )

    return es_result
# 裁判文书网更新值
def getmysql_cpws():
    # 日期

    yesterday = str(datetime.date.today() + datetime.timedelta(days=-1))
    qiantian = str(datetime.date.today() + datetime.timedelta(days=-2))

    # 连接mysql
    try:
        sql = "SELECT MAX(dayadd_count) FROM dayadd WHERE create_time >= " + "'" + qiantian +" 01:00:00"+ "'" + "and create_time <" + "'" + yesterday +" 00:05:00"+"'"
        cursor.execute(sql)
        conn.commit()
    except Exception:
        print(traceback.format_exc())
    results = cursor.fetchall()
    dict_a = results[0][0]
    mysql_count_dayadd = ""
    if dict_a:
        mysql_count_dayadd = json.loads(str(dict_a))
    return mysql_count_dayadd

def getES_cpws(es):
    # 日期

    yesterday = str(datetime.date.today() + datetime.timedelta(days=-1))
    yesterday_zone = yesterday + "T00:00:00+08:00"
    qiantian = str(datetime.date.today() + datetime.timedelta(days=-2))
    qiantian_zone = qiantian + "T00:00:00+08:00"
    res = es.count(
        index='judge_doc',
        doc_type='wenshuwang_doc',
        body={
            "query": {
                "bool": {
                    "filter": {
                        "range": {
                            "publish_date": {"gte": qiantian_zone, "lt": yesterday_zone}
                        }
                    }
                }
            }
        }
    )

    count_num = res['count']
    return  count_num

# 日环比增长
def types_daily_increase(index,doc_type,date_str,query_time_type):
    # 日期
    today_zone = date_str + "T23:59:59+08:00"
    tmp_datetime = time.strptime(date_str, "%Y-%m-%d")
    y, m, d = tmp_datetime[0:3]
    yesterday = str(datetime.date(y, m, d) + datetime.timedelta(days=-1))
    yesterday_zone = yesterday + "T00:00:00+08:00"


    # 查询语句
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
                    },
                    {
                      "range": {
                        "%s": {
                          "gte": "%s",
                          "lt": "%s"
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
                "2": {
                  "date_histogram": {
                    "field": "%s",
                    "interval": "1d",
                    "time_zone": "Asia/Shanghai",
                    "min_doc_count": 1
                  }
                }
              }
            }
    """%(query_time_type,yesterday_zone,today_zone,query_time_type)

    es_result = es.search(
            body=query,
            index=index,
            doc_type=doc_type,
            scroll="5m",
            timeout="1m",
    )
    return es_result

# 将每种类型的数据封装到types2day_increase_dict 字典中
def tongji_type2days_increase(index,doc_type,date_str,types2day_increase_dict):
    # 日
    tmp_time_str = time.strptime(date_str, "%Y-%m-%d")
    y, m, d = tmp_time_str[0:3]
    date_str_1 = str(datetime.date(y, m, d))
    date_str_2 = str(datetime.date(y, m, d) + datetime.timedelta(days=-1))

    # 对query_time_type 的处理
    query_time_type='update_time'
    if index in ['court_session_announcement','court_announcement']:
        query_time_type='create_time'

    es_result = types_daily_increase(index, doc_type, date_str, query_time_type)
    item_list = es_result['aggregations']['2']['buckets']
    # 每个日期
    types2day_increase_dict[index] = {}
    # 每天的value的初始化
    # for i in range(1,duration+2):
        # range_day = str(datetime.date.today() + datetime.timedelta(days=-i))
    types2day_increase_dict[index][date_str_1] = 0
    types2day_increase_dict[index][date_str_2] = 0
    for item in item_list:
        date = item['key_as_string'][:10]
        doc_count = item['doc_count']
        types2day_increase_dict[index][date] = doc_count


# 计算一天的增长率
def calculate_ratio(date_str):
    # 统计了每个index每天增长
    index2type_dict = {
        "judge_doc": "total_doc",
        "court_announcement": "court_announcement",
        "shixin_beizhixing": "shixin_beizhixing_total",
        "court_session_announcement": "court_session_announcement",
        "exposure_desk": "exposure_desk",
        "executive_announcement": "executive_announcement_total"
    }
    # 对所有数据的封装
    types2day_increase_dict = {}
    for index, doc_type in index2type_dict.items():
        tongji_type2days_increase(index, doc_type, date_str, types2day_increase_dict)
    # 计算出每天总量的增长
    total2day_increase_dict = {}
    for type, item_dict in types2day_increase_dict.items():
        for date, doc_count in item_dict.items():
            try:
                total2day_increase_dict[date] += doc_count
            except:
                total2day_increase_dict[date] = 0
                total2day_increase_dict[date] += doc_count
    # 计算日环比增长率
    total2day_increase_ratio_dict = {}

    tmp_datetime = time.strptime(date_str, "%Y-%m-%d")
    y, m, d = tmp_datetime[0:3]
    date_one = str(datetime.date(y, m, d) + datetime.timedelta(days=-1))
    # 昨天的count
    doc_count_1 = total2day_increase_dict[date_str]
    # 前天的count
    doc_count__2 = total2day_increase_dict[date_one]
    if doc_count__2 <=0 :
        ratio = 1
    else:
        ratio = (doc_count_1 - doc_count__2) / doc_count__2

    total2day_increase_ratio_dict['date'] = date_str
    ratio = float('%.4f' % ratio)
    total2day_increase_ratio_dict['ratio'] = ratio
    # 存到mysql
    d = daily_increase_ratio()
    d.as_of_day=date_str
    d.value=ratio
    d.data_type=0
    d.record_type=0
    d.save()

    return total2day_increase_ratio_dict