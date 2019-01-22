from django.db import models

# Create your models here.

class manual_crawler_info(models.Model):

    #　crawler_type 裁判文书，失信被执行，被执行人
    crawler_type = models.CharField(max_length=100)
    # type 1:企业名　2:人名
    type = models.IntegerField()
    # name
    ent_person_name = models.CharField(max_length=100)
    # create_time 创建时间
    create_time = models.DateTimeField(auto_now=True)
    # flag_status 0是没有完成　1是正在爬去　2　是完成了
    flag_status = models.IntegerField()






