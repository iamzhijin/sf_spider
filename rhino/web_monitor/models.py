from django.db import models

# Create your models here.

class webMonitor_resultNum(models.Model):

    # 网站名称
    web_name = models.CharField(max_length=255,db_index=True,primary_key=True)
    # 本次爬取数量
    web_num = models.CharField(max_length=255,default="")
    # es数量
    es_num = models.CharField(max_length=255,default="")
    # date
    web_date_start = models.CharField(max_length=255,default="")
    # 状态
    status = models.CharField(max_length=255,default="")
    # data_type
    data_type = models.CharField(max_length=255,default="")

class webMonitor_task(models.Model):
    # 网站名称
    web_name = models.CharField(max_length=255,db_index=True,primary_key=True)
    # 数据类型：裁判文书，开庭公告等
    data_type = models.CharField(max_length=255, db_index=True)
    # 爬取网址
    web_site = models.CharField(max_length=255)
    # 爬取方法
    request_function = models.CharField(max_length=255)
    # 爬取参数
    request_body = models.CharField(max_length=255)
    # xpath 表达式 和re表达式
    xpath_str = models.CharField(max_length=255)
    re_str = models.CharField(max_length=255)
    # response_type：HTML&INTERFACE
    response_type = models.CharField(max_length=255)
    # keyword 字段
    keyword = models.CharField(max_length=255)
    # 每页多少个
    per_num = models.IntegerField(default=0)
    # 创建时间
    web_update_time = models.DateTimeField(auto_now=True)
    # 地区法院名称
    region_web_name = models.CharField(max_length=255, db_index=True, default="")