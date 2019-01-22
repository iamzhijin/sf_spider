from django.conf.urls import url
from . import views,views_interface
from django.views.generic.base import TemplateView



app_name = 'monitor'

urlpatterns = [
    # 提交监控信息
    url(r'^crawData_check_result',views.crawData_check_result,name='crawData_check_result'),
    url(r'^add_monitor', views.add_monitor,name='add_monitor'),
    url(r'^monitor_list$',views.monitor_list,name='monitor_list'),
    url(r'^monitor_list_api$',views.monitor_list_api,name='monitor_list_api'),
    url(r'^start_monitorHTML',views.start_monitorHTML,name='start_monitorHTML'),
    url(r'^lanch_monitor',views.lanch_monitor,name='lanch_monitor'),
    url(r'^lanch_cmp',views.lanch_cmp,name='lanch_cmp'),
    url(r'^stop_monitor',views.stop_monitor,name='stop_monitor'),
    url(r'^deleteCrawDataInfo',views.deleteCrawDataInfo,name='deleteCrawDataInfo'),

    # ====大屏接口=====
    url(r'^crawler/alert$', views_interface.alert, name='alert'),
    url(r'^crawler/stat/history$', views_interface.stat_history, name='stat_history'),
    url(r'^crawler/stat/overview$', views_interface.stat_overview, name='stat_overview'),
    url(r'^crawler/stat/daily_increase_ratio',views_interface.daily_increase_ratio_api,name='daily_increase_ratio_api'),
    # ====大屏展示=====
    url(r'^show_big_screen$',views.show_big_screen,name='show_big_screen'),
    # ====错误的爬虫=====
    url(r'^show_warning_crawl$', views.check_web_status, name='check_web_status'),
    url(r'^await_warning$', views.await_warning, name='await_warning'),
    url(r'^no_warning$', views.no_warning, name='no_warning'),


    # 大屏展示接口 
    # 每个项目每天更新的数量
    url(r'^project_update_by_day$', views.project_update_by_day, name="project_update_by_day"),
    url(r'^crawl_total$', views.crawl_total, name="crawl_count"),
    url(r'^project_all_total$', views.project_all_total, name="project_all_total"),
    url(r'^crawled_uncrawled_project$', views.crawled_uncrawled_project, name="crawled_uncrawled_project"),
    url(r'^test_celery$', views.test_celery, name="test_celery "),
    url(r'^test_celery_fetcher', views.test_celery_fetcher, name="test_celery_fetcher "),
    url(r'^crawler_info', views.crawler, name="crawler_info"),
    url(r'^field_mapping', views.field_mapping, name="field_mapping"),
    url(r'^update_crawler', views.update_crawler, name="update_crawler"),


]
