from django.db import models
from CrawlProject.models import Project
import uuid
import os

def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext) 
    return os.path.join(instance.id, filename) # 使用os拼接文件名以适应不同系统

class Crawls(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, db_column="project_id", related_name="project")
    crawl_name = models.CharField("爬虫名称", max_length=30)
    code = models.CharField("爬虫编码", max_length=50, null=True)
    crawl_file = models.FileField("爬虫文件", upload_to=upload_to, max_length=50)
    source = models.CharField("爬虫源网站", max_length=100)
    create_time = models.DateTimeField("创建日期", auto_now_add=True)
    update_time = models.DateTimeField("更新日期", auto_now=True)

    def __str__(self):
        return self.crawl_name   

    class Meta:
        db_table = 'crawls'
        ordering = ['-update_time']
