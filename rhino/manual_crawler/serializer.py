#! /user/bin/env python
# ——×—— coding:utf-8 ——×——

from rest_framework import serializers,viewsets

class manualCrawlerSerialzers(serializers.Serializer):
    id = serializers.IntegerField()
    # 　crawler_type 裁判文书，失信被执行，被执行人
    crawler_type = serializers.CharField(max_length=10)
    # type 1:企业名　2:人名
    type = serializers.IntegerField()
    # name
    ent_person_name = serializers.CharField(max_length=100)
    # create_time 创建时间
    create_time = serializers.DateTimeField()
    # flag_status 0是没有完成　1是正在爬去　2　是完成了
    flag_status = serializers.IntegerField()
