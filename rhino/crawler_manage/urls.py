from django.conf.urls import url
from django.conf.urls import include
from . import views
from . import views_project
from . import views_crawler
from . import views_task
from . import views_server
from . import views_processor

app_name = 'crawler_manage'

urlpatterns = [
    url(r'^list_project$', views.list_projects, name='list_projects'),
    url(r'project_detail/(?P<project_id>[0-9A-Za-z_]+)$', views.show_project, name='show_project'),

    ###########项目相关###########
    url(r'^project/create$', views_project.project_create, name='project_create'),
    url(r'^project/list$', views_project.project_list_page, name='project_list'),
    #api
    url(r'^project/api/project_list$', views_project.project_list_api, name='api_list'),

    ###########爬虫相关#############
    url(r'^crawler/create$', views_crawler.crawler_create, name='crawler_create'),
    url(r'^crawler/(?P<crawler_id>[0-9A-Za-z_]+)/tasks$', views_crawler.crawler_tasks, name='crawler_tasks'),
    url(r'^crawler/delete/(?P<crawler_id>[0-9A-Za-z_]+)$', views_crawler.crawler_delete, name='crawler_delete'),
    url(r'^crawler/edit/(?P<crawler_id>[0-9A-Za-z_]+)$', views_crawler.crawler_edit, name='crawler_edit'),
    url(r'^crawler/edit_submit$', views_crawler.crawler_edit_submit, name='crawler_edit_submit'),
    url(r'^crawler/list$', views_crawler.crawler_list, name='crawler_list'),
    url(r'^crawler/api/crawler_list$', views_crawler.crawler_list_api, name='crawler_list_api'),
    url(r'^crawler/crawler_app/(?P<crawler_id>[0-9A-Za-z_]+)$', views_crawler.view_crawler_app, name='view_crawler_app'),

    ###########任务相关#############
    url(r'^task/create$', views_task.task_create, name='task_create'),
    url(r'^task/create_submit$', views_task.task_create_submit, name='task_create_submit'),
    url(r'^task/list$', views_task.task_list, name='task_list'),
    url(r'^task/edit/(?P<task_id>[0-9A-Za-z_-]+)$', views_task.task_edit, name='task_edit'),
    url(r'^task/log/(?P<task_id>[0-9A-Za-z_-]+)$', views_task.task_log, name='task_log'),
    url(r'^task/edit_submit$', views_task.task_edit_submit, name='task_edit_submit'),
    url(r'^task/crawler_start/(?P<task_server_id>[0-9A-Za-z_-]+)$', views_task.crawler_start, name='task_crawler_start'),
    url(r'^task/crawler_stop/(?P<task_server_id>[0-9A-Za-z_-]+)$', views_task.crawler_stop, name='task_crawler_stop'),
    url(r'^task/backup_start/(?P<task_id>[0-9A-Za-z_-]+)$', views_task.backup_start, name='task_backup_start'),
    url(r'^task/backup_stop/(?P<task_id>[0-9A-Za-z_-]+)$', views_task.backup_stop, name='task_backup_stop'),
    url(r'^task/clean_start/(?P<task_id>[0-9A-Za-z_-]+)$', views_task.clean_start, name='task_clean_start'),
    url(r'^task/clean_stop/(?P<task_id>[0-9A-Za-z_-]+)$', views_task.clean_stop, name='task_clean_stop'),
    url(r'^task/delete/(?P<task_id>[0-9A-Za-z_-]+)$', views_task.task_delete, name='task_delete'),
    #api
    url(r'^task/api/detail/(?P<task_id>[0-9A-Za-z_-]+)$', views_task.task_detail_api, name='task_detail_api'),
    url(r'^task/api/list$', views_task.task_list_api, name='task_list_api'),
    url(r'^task/validate_rules/(?P<task_id>[0-9A-Za-z_]+)$', views_task.get_validate_rules, name='get_validate_rules'),
    url(r'^task/api/status/(?P<task_id>[0-9A-Za-z_]+)$', views_task.task_status_api, name='task_status_api'),

    ############服务器相关############
    url(r'^server/create$', views_server.create_server, name='server_create'),
    url(r'^server/create_submit$', views_server.create_server_submit, name='server_create_submit'),
    url(r'^server/list$', views_server.list_server, name='server_list'),
    url(r'^server/api/list$', views_server.list_server_api, name='list_server_api'),

    ############通用清洗处理相关#######
    url(r'^processor/create$', views_processor.processor_create, name='processor_create'),
    url(r'^processor/(?P<processor_id>[0-9A-Za-z_]+)/crawlers$', views_processor.processor_tasks, name='processor_tasks'),
    url(r'^processor/delete/(?P<processor_id>[0-9A-Za-z_]+)$', views_processor.processor_delete, name='processor_delete'),
    url(r'^processor/create_submit$', views_processor.processor_create_submit, name='processor_create_submit'),
    url(r'^processor/edit/(?P<processor_id>[0-9A-Za-z_-]+)$', views_processor.processor_edit, name='processor_edit'),
    url(r'^processor/edit_submit$', views_processor.processor_edit_submit, name='processor_edit_submit'),
    url(r'^processor/list$', views_processor.processor_list, name='processor_list'),
    #api
    url(r'^processor/api/list$', views_processor.processor_list_api, name='processor_list_api'),
    url(r'^processor/api/detail/(?P<processor_id>[0-9A-Za-z_-]+)$', views_processor.processor_detail_api, name='processor_list_api'),
    url(r'^processor/start/(?P<processor_id>[0-9A-Za-z_-]+)$', views_processor.processor_start, name='processor_clean_start'),
    url(r'^processor/stop/(?P<processor_id>[0-9A-Za-z_-]+)$', views_processor.processor_stop, name='processor_clean_stop'),
]

