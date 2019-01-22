# coding=utf-8

# Author: Ron Lin
# Date: 2017/9/14
# Email: hdsmtiger@gmail.com

from rest_framework import serializers
from .models import ValidateRule
from .models import Project


class ValidateRuleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    task_id = serializers.CharField(read_only=True)
    field_name = serializers.CharField(read_only=True)
    rule = serializers.CharField(read_only=True)
    desc = serializers.StringRelatedField(read_only=True)
    type = serializers.IntegerField()
    create_time = serializers.DateTimeField(read_only=True)
    # class Meta:
    #     model = ValidateRule
    #     fields = ("task_id", "field_name", "rule", "desc", "type", "create_time")

    # def create(self, validated_data):
    #     """
    #     Create and return a new `Snippet` instance, given the validated data.
    #     """
    #     return ValidateRule.objects.create(**validated_data)


class ProjectSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    code = serializers.CharField()
    project_name = serializers.CharField()
    desc = serializers.CharField()
    create_time = serializers.DateTimeField()
    update_time = serializers.DateTimeField()

    def create(self, validated_data):
        return Project.objects.create(**validated_data)


class CrawlerSerializer(serializers.Serializer):
    id = serializers.CharField()
    crawler_name = serializers.CharField()
    project_id = serializers.CharField()
    project_name = serializers.CharField()
    crawler_app = serializers.CharField()
    clean_app = serializers.CharField()
    clean_parameters = serializers.CharField()
    need_clean = serializers.BooleanField()
    create_time = serializers.DateTimeField()
    update_time = serializers.DateTimeField()
    fields_mapping = serializers.CharField()
    clean_method = serializers.CharField()
    processor_id = serializers.CharField()
    processor_name = serializers.CharField()
    web_title = serializers.CharField()
    web_url = serializers.CharField()
    update_strategy = serializers.CharField()  # 下拉框后面在改
    use_for = serializers.CharField()
    crawl_owner = serializers.CharField()
    count = serializers.CharField()
    time_limit = serializers.CharField()
    source = serializers.CharField()

class TaskSerializer(serializers.Serializer):
    id = serializers.CharField()
    project_id = serializers.CharField()
    project_name = serializers.CharField()
    crawler_id = serializers.CharField()
    crawler_name = serializers.CharField()
    crawler_app = serializers.CharField()
    clean_app = serializers.CharField()
    crawler_parameters = serializers.CharField()
    clean_parameters = serializers.CharField()
    fields_mapping = serializers.CharField()
    need_clean = serializers.BooleanField()
    deploy_target = serializers.CharField()
    general_clean_rules = serializers.CharField()
    status = serializers.IntegerField()
    clean_app_status = serializers.IntegerField()
    data_backup_status = serializers.IntegerField()
    create_time = serializers.DateTimeField()
    update_time = serializers.DateTimeField()
    start_time = serializers.DateTimeField()
    stop_time = serializers.DateTimeField()
    servers = serializers.CharField()
    clean_method = serializers.CharField()
    processor_id = serializers.CharField()
    processor_name = serializers.CharField()


class SpiderServerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    host = serializers.CharField()
    port = serializers.IntegerField()
    type = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()
    create_time = serializers.DateTimeField()
    update_time = serializers.DateTimeField()


class ProcessorSerializer(serializers.Serializer):
    id = serializers.CharField()
    project_id = serializers.CharField()
    project_name = serializers.CharField()
    processor_name = serializers.CharField()
    clean_app = serializers.CharField()
    clean_parameters = serializers.CharField()
    fields_mapping = serializers.CharField()
    deploy_target = serializers.CharField()
    general_clean_rules = serializers.CharField()
    create_time = serializers.DateTimeField()
    update_time = serializers.DateTimeField()
