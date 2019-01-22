from django.db import models
from crawler_manage.models import Crawler


class CrawDataInfo(models.Model):
    province = models.CharField(max_length=20)
    ent_name = models.CharField(max_length=50)
    content = models.TextField(default='')
    create_time = models.DateTimeField(auto_now=True)
    update_time = models.DateTimeField(auto_now=True)
    # def __str__(self):
    #     return self.ent_name


class TestResultInfo(models.Model):
    test_count = models.IntegerField()
    correct_count = models.IntegerField()
    error_count = models.IntegerField()
    error_entName =  models.TextField(default='')
    create_time = models.DateTimeField(auto_now=True)


class daily_increase_ratio(models.Model):
    # as_of_day:date 计算当天
    # value:double 记录值
    id = models.AutoField(primary_key=True)
    as_of_day = models.DateField(db_index=True)
    value = models.FloatField()
    # record_type：smallint 记录类型 （可选值：0-日环比增长率，1-日增长率， 2，日增加数据量）
    record_type = models.IntegerField(db_index=True)
    # data_type: smallint 数据类型 （可选值：0-总数据，1-开庭公告，2-被执行人，3-失信被执行人，4-裁判文书，5-法院公告，6-曝光台）
    data_type = models.IntegerField(db_index=True)

    class Meta:
        unique_together = ("as_of_day", "record_type", "data_type")



class CrawlWarning(models.Model):

    id = models.AutoField(primary_key=True)
    crawl = models.ForeignKey(Crawler,on_delete=models.CASCADE)
    """监控策略, 通过celery后台进行监控."""
    # requests web status_code; if exception return 600
    crawler_name = models.CharField(max_length=200, unique=True, null=False, default='')
    web_status = models.CharField(null=True, max_length=30)
    crawl_time = models.DateField(null=True)   # 爬虫出错的时间
    warn_time = models.DateField(null=True)  # 预警时间
    status = models.CharField(max_length=200, null=True)  # 0 未修复, 1 人工修复, 2 自动修复, 3 数据源废弃; 暂停预警, 解除预警

