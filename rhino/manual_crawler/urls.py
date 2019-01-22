#! /user/bin/env python
# ——×—— coding:utf-8 ——×——
from django.conf.urls import url
from . import views,views_export

app_name = 'manual_crawler'

urlpatterns = [
    # url(r'^manual_crawler_create',views.manual_crawler_create,name='manual_crawler_create'),
    url(r'^manual_crawler_show',views.manual_crawler_show,name='manual_crawler_show'),
    # url(r'^triggle_crawler',views.triggle_crawler,name='triggle_crawler'),
    url(r'^submit_crawler',views.submit_crawler,name='submit_crawler'),
    url(r'^crawler_list_api',views.crawler_list_api,name='crawler_list_api'),
    url(r'^delete_manual_crawler',views.delete_manual_crawler,name='delete_manual_crawler'),
    # url(r'^triggle_crawler',views.triggle_crawler,name='triggle_crawler'),

    #
    url(r'^run_manual_crawler',views.run_manual_crawler,name='run_manual_crawler'),

    url(r'^go2export_ent_sifa_info', views_export.go2export_ent_sifa_info, name='go2export_ent_sifa_info'),
    url(r'^export_ent_sifa_info', views_export.export_ent_sifa_info, name='export_ent_sifa_info')
]


