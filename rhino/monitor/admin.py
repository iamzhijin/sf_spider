from django.contrib import admin
from .models import *
# Register your models here.





class CrawDataInfoAdmin(admin.ModelAdmin):
    # 显示字段
    list_display = ['id','province','ent_name','content','create_time','update_time']
    # 过滤字段
    list_filter = ['province']
    # 搜索字段
    search_fields = ['ent_name']
    # 分页
    list_per_page = 30


admin.site.register(CrawDataInfo,CrawDataInfoAdmin)


