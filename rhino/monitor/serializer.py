#!/usr/bin/env python
# -*- coding:utf-8 -*-
from rest_framework import serializers
from .models import daily_increase_ratio
from crawler_manage.serializer import CrawlerSerializer
class CrawDataInfoSerializer(serializers.Serializer):

    province = serializers.CharField()
    ent_name = serializers.CharField()
    create_time = serializers.DateTimeField()
    update_time = serializers.DateTimeField()

class daily_increase_ratioSerializer(serializers.Serializer):
    # as_of_day:date 计算当天
    # value:double 记录值
    as_of_day = serializers.DateField()
    value = serializers.FloatField()
    # record_type：smallint 记录类型 （可选值：0-日环比增长率，1-日增长率， 2，日增加数据量）
    record_type = serializers.IntegerField()
    # data_type: smallint 数据类型 （可选值：0-总数据，1-开庭公告，2-被执行人，3-失信被执行人，4-裁判文书，5-法院公告，6-曝光台）
    data_type = serializers.IntegerField()

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return daily_increase_ratio.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.as_of_day = validated_data.get('as_of_day', instance.as_of_day)
        instance.value = validated_data.get('value', instance.value)
        instance.record_type = validated_data.get('record_type', instance.record_type)
        instance.data_type = validated_data.get('data_type', instance.data_type)
        instance.save()
        return instance


class CrawlWarningSerializer(serializers.Serializer):
    id = serializers.CharField()
    crawl = CrawlerSerializer()
    """监控策略, 通过celery后台进行监控."""
    # requests web status_code; if exception return 600
    web_status = serializers.CharField()
    status = serializers.CharField()
    crawler_name = serializers.CharField()
    crawl_time = serializers.CharField()
    warn_time = serializers.CharField()