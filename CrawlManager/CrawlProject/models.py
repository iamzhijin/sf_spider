from django.db import models


class Project(models.Model):
    project_name = models.CharField("项目名称", max_length=30)
    describe = models.TextField("项目描述", null=True)
    code = models.CharField("项目编码", max_length=10)
    create_time = models.DateTimeField("项目创建时间", auto_now_add=True)
    update_time = models.DateTimeField("项目更新时间", auto_now=True)

    def __str__(self):
        return self.project_name

    class Meta:
        db_table = "project"
        ordering = ["-create_time"]