from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import webMonitor_task,webMonitor_resultNum
import datetime
from .views import do_monitor



# 爬去网页数据，并保存
@shared_task
def crawler_web_num():
    webMonitorInfo_list = webMonitor_task.objects.all()
    count =0
    today = str(datetime.date.today())
    for item in webMonitorInfo_list:
        count += 1
        print(count)
        web_name = item.web_name
        print(web_name)
        data_type = item.data_type
        web_site = item.web_site
        request_function = item.request_function
        request_body = item.request_body
        response_type = item.response_type
        xpath_str = item.xpath_str
        re_str = item.re_str
        keyword = item.keyword
        per_num = item.per_num
        tmp_dict = do_monitor(web_name, web_site, request_function, request_body, response_type, xpath_str, re_str,
                              keyword,
                              per_num)
        num = tmp_dict['num']
        # save num
        w = webMonitor_resultNum()
        w.web_name=web_name
        w.web_num=num
        w.web_date_start=today
        w.data_type=data_type
        w.save()




        # 对比数据