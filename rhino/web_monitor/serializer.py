#! /user/bin/env python
# ——×—— coding:utf-8 ——×——

from rest_framework import serializers,viewsets

class webMonitor_resultNum_Serializers(serializers.Serializer):

    # 网站名称
    web_name = serializers.CharField(max_length=255)
    # 本次爬取数量
    web_num = serializers.CharField(max_length=255)
    # es数量
    es_num = serializers.CharField(max_length=255)
    # date
    web_date_start = serializers.CharField(max_length=255)

    # 状态
    status = serializers.CharField(max_length=255)
    data_type = serializers.CharField(max_length=255)

class webMonitor_taskSerializers(serializers.Serializer):
    # 网站名称
    web_name = serializers.CharField(max_length=255)
    # 地区法院名称
    region_web_name = serializers.CharField(max_length=255)
    # 数据类型：裁判文书，开庭公告等
    data_type = serializers.CharField(max_length=255)
    # 爬取网址
    web_site = serializers.CharField(max_length=255)
    # 爬取方法
    request_function = serializers.CharField(max_length=255)
    # 爬取参数
    request_body = serializers.CharField(max_length=255)
    # xpath 表达式 和re表达式
    xpath_str = serializers.CharField(max_length=255)
    re_str = serializers.CharField(max_length=255)
    # response_type：HTML&INTERFACE
    response_type = serializers.CharField(max_length=255)
    # keyword 字段
    keyword = serializers.CharField(max_length=255)
    # 每页多少个
    per_num = serializers.IntegerField(default=-1)
    # 创建时间
    web_update_time = serializers.DateTimeField()