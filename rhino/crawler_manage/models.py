from django.db import models
from django.utils.encoding import python_2_unicode_compatible
# Create your models here.


def decode(info):
    return info.decode('utf-8')



@python_2_unicode_compatible
class Project(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=20, db_index=True, unique=True)
    # es表的地址  judge_doc/total_doc
    es_table = models.CharField(max_length=200, default='')
    project_name = models.CharField(max_length=100, db_index=True)
    desc = models.TextField(max_length=1000, default='')
    create_time = models.DateTimeField(db_index=True, auto_now=True)
    update_time = models.DateTimeField(db_index=True, auto_now=True)

    def __str__(self):
        return "project_name: {}".format(self.project_name)
                


@python_2_unicode_compatible
class Crawler(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    crawler_name = models.CharField(max_length=100, db_index=True)
    project_id = models.CharField(max_length=100)
    project_name   = models.CharField(max_length=100)
    crawler_app    = models.URLField(max_length=200)
    clean_app      = models.URLField(max_length=200)
    clean_parameters = models.TextField(max_length=500)
    fields_mapping = models.TextField(max_length=10240)
    need_clean     = models.BooleanField(default=False)
    clean_method   = models.CharField(max_length=10, db_index=True, default='custom')
    processor_id   = models.CharField(max_length=100, db_index=True, default='')
    processor_name = models.CharField(max_length=100, default='')
    create_time    = models.DateTimeField(db_index=True, auto_now=True)
    update_time    = models.DateTimeField(db_index=True, auto_now=True)
    # 后面字段需要像业务人员展示, 先定义为空
    web_title = models.CharField(max_length=200, null=True)
    web_url = models.URLField(max_length=200, null=True)
    update_strategy = models.CharField(max_length=200, null=True)  # 下拉框后面在改
    use_for = models.CharField(max_length=200, null=True)
    crawl_owner = models.CharField(max_length=200, null=True)
    count = models.CharField(max_length=200, null=True)
    time_limit = models.DateField(default='9999-9-9')
    source = models.CharField(max_length=200, null=True)

    def __str__(self):
        return "crawler_name: {}".format(self.crawler_name)
               

@python_2_unicode_compatible
class SpiderServer(models.Model):
    id = models.AutoField(primary_key=True)
    host = models.CharField(max_length=50)
    port = models.IntegerField()
    type = models.CharField(max_length=50, db_index=True)
    username = models.CharField(max_length=50, default="")
    password = models.CharField(max_length=50, default="")
    create_time = models.DateTimeField(db_index=True, auto_now=True)
    update_time = models.DateTimeField(db_index=True, auto_now=True)

@python_2_unicode_compatible
class Task(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    project_id = models.CharField(max_length=100, db_index=True)
    crawler_id = models.CharField(max_length=100, db_index=True)
    crawler_name = models.CharField(max_length=100, db_index=True)
    project_name = models.CharField(max_length=100)
    clean_method = models.CharField(max_length=10, db_index=True, default='custom')
    processor_id = models.CharField(max_length=100, db_index=True, default='')
    processor_name = models.CharField(max_length=100, default='')
    crawler_app = models.URLField(max_length=200)
    crawler_parameters = models.TextField(max_length=500)
    clean_app = models.URLField(max_length=200)
    clean_parameters = models.TextField(max_length=500)
    fields_mapping = models.TextField(max_length=10240)
    need_clean = models.BooleanField(default=False)
    deploy_target = models.CharField(max_length=500, default='', null=True)
    general_clean_rules = models.CharField(max_length=1000, default='')
    status = models.IntegerField(default=0, db_index=True) #废弃，不用
    clean_app_status = models.IntegerField(default=0, db_index=True) #废弃，不用
    data_backup_status = models.IntegerField(default=0, db_index=True) #废弃，不用
    servers = models.CharField(max_length=200, default='')  #废弃，不用
    start_time = models.DateTimeField(db_index=True, null=True)
    stop_time = models.DateTimeField(db_index=True, null=True)
    create_time = models.DateTimeField(db_index=True, auto_now=True)
    update_time = models.DateTimeField(db_index=True, auto_now=True)

    def __str__(self):
        return "id: {}".format(self.id)
               
@python_2_unicode_compatible
class TaskServer(models.Model):
    task = models.ForeignKey(Task,on_delete=models.CASCADE)
    server = models.ForeignKey(SpiderServer,on_delete=models.CASCADE)
    create_time = models.DateTimeField(db_index=True, auto_now=True)

    class Meta:
        unique_together = ("task", "server")

    def __str__(self):
        return "task_id: {} and server_id: {}".format(self.task_id, str(self.server_id))


@python_2_unicode_compatible
class ValidateRule(models.Model):
    id = models.AutoField(primary_key=True)
    task_id = models.CharField(max_length=100, db_index=True)
    field_name = models.CharField(max_length=100)
    rule = models.CharField(max_length=100)
    type = models.SmallIntegerField()
    desc = models.TextField(max_length=200)
    create_time = models.DateTimeField(db_index=True, auto_now=True)

    # class Meta:
    #     unique_together = ("task_id", "field_name")

    def __str__(self):
        return self.desc + " task id: " + self.task_id + " field: " + self.field_name


@python_2_unicode_compatible
class Processor(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    project_id = models.CharField(max_length=100, db_index=True)
    project_name = models.CharField(max_length=100)
    processor_name = models.CharField(max_length=100, db_index=True)
    clean_app = models.URLField(max_length=200)
    clean_parameters = models.TextField(max_length=500)
    fields_mapping = models.TextField(max_length=10240)
    deploy_target = models.CharField(max_length=500, default='', null=True)
    general_clean_rules = models.TextField(max_length=10240, default='')
    create_time = models.DateTimeField(db_index=True, auto_now=True)
    update_time = models.DateTimeField(db_index=True, auto_now=True)

    def __str__(self):
        return self.id + ': ' + self.processor_name


# pyspider model, 使用不同的mysql数据库
@python_2_unicode_compatible
class SpiderTask(models.Model):
    taskid = models.CharField(max_length=64, primary_key=True)
    project = models.CharField(max_length=64)
    url = models.CharField(max_length=1024)
    status = models.IntegerField()
    schedule = models.BinaryField(max_length=64)
    fetch = models.BinaryField(max_length=64)
    process = models.BinaryField(max_length=64)
    track = models.BinaryField(max_length=64)
    lastcrawltime = models.FloatField()
    updatetime = models.FloatField()
