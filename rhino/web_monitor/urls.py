#! /user/bin/env python
# ——×—— coding:utf-8 ——×——
from django.conf.urls import url
from . import views,views_compare
app_name = 'web_monitor'

urlpatterns = [
    # 创建监控
    url(r'^go2create_web_monitor_html',views.go2create_web_monitor_html,name='go2create_web_monitor_html'),
    # 显示 show_web_monitor.html
    url(r'^show_web_monitor',views.show_web_monitor,name='show_web_monitor'),
    # 测试按钮
    url(r'^test_web_monitor_task',views.test_web_monitor_task,name='test_web_monitor_task'),
    # 监控列表
    url(r'^web_monitor_list_api',views.web_monitor_list_api,name='web_monitor_list_api'),
    # 创建监控任务（插入mysql）
    url(r'^create_web_monitor_task',views.create_web_monitor_task,name='create_web_monitor_task'),
    # 删除监控任务
    url(r'^delete_web_monitor',views.delete_web_monitor,name='delete_web_monitor'),
    # 执行监控任务
    url(r'^run_web_monitor_task',views.run_web_monitor_task,name='run_web_monitor_task'),
    # 结果给列表页的btsp table
    url(r'^results_web_monitor_list_api',views.results_web_monitor_list_api,name='results_web_monitor_list_api'),
    # 跳转到results_web_monitor.html
    url(r'^results_web_monitor',views.results_web_monitor,name='results_web_monitor'),
    # 删除监控数据
    url(r'^delete_results_web_monitor',views.delete_results_web_monitor,name='delete_results_web_monitor'),
    #====================对比任务=================
    # 跳转页面
    url(r'^go2manual_trigger_web_monitor',views_compare.go2manual_trigger_web_monitor,name='go2manual_trigger_web_monitor'),
    url(r'^manual_trigger_web_monitor',views_compare.manual_trigger_web_monitor,name='manual_trigger_web_monitor'),


]


