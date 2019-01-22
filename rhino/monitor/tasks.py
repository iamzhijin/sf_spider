from __future__ import absolute_import
from celery import shared_task
from monitor.models import CrawlWarning
import requests
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from crawler_manage.models import Project
from crawler_manage.models import Crawler
from monitor.es_search import EsMan
from datetime import date
from datetime import timedelta
import time

# 后台任务, 扫描所有crawl的url, 判断请求url状态码
@shared_task
@periodic_task(run_every=crontab(minute=0, hour='*/3'))
def celery_fetcher():
    today = date.today()
    crawlers = Crawler.objects.all()
    for crawler in crawlers:
        crawler_name = crawler.crawler_name
        crawl_id = crawler.id
        if crawler.web_url:
            flag = 0
            while flag <= 3:
                try:
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36'
                    }
                    response = requests.get(crawler.web_url, headers=headers, timeout=30)
                    web_status = response.status_code
                    if web_status < 400:
                        break
                except:
                    time.sleep(1)
                    web_status = 555
            print(crawler.web_url, web_status)
            cws = CrawlWarning.objects.filter(crawler_name=crawler.crawler_name)
            if web_status >= 400:
                if cws:
                    cws = cws[0]
                    if cws.status == '0':
                        cws.web_status = web_status
                        cws.save()

                    elif cws.status == '2':
                        cws.status = '0'
                        cws.warn_time = today
                        cws.web_status = web_status
                        cws.save()

                else:
                    cws = CrawlWarning(status='0', warn_time=today, crawl_time=today, web_status=web_status, crawl_id=crawl_id,
                                       crawler_name=crawler_name)
                    cws.save()

            else:
                if cws and cws[0].status == '0':
                    cws = cws[0]
                    cws.status = '2'
                    cws.warn_time = today
                    cws.save()



# @periodic_task(run_every=crontab(minute=0, hour=0))    @periodic_task(run_every=crontab())
#minute=0, hour=0
@shared_task
@periodic_task(run_every=crontab(minute=0, hour='*/3'))
def celery_check_update_interval():
    today = date.today()
    projects = Project.objects.all()
    es = EsMan()

    for project in projects:
        url = project.es_table
        if url and '/' in url:
            for item in es.source_sort_by_time(url):
                source, es_crawl_time = item['source'], item['crawl_time']

                interval = (date.today() - timedelta(days=1) - es_crawl_time).days
                try:
                    crawler = Crawler.objects.filter(source=source, project_id=project.code)
                    crawler_name = crawler[0].crawler_name
                    crawler_id = crawler[0].id
                    cws = CrawlWarning.objects.select_related('crawl').filter(crawl__source=source)

                    if interval > 0:
                        if cws:
                            cws = cws[0]
                            if cws.status == '2':
                                cws.status = '0'
                                cws.warn_time = today
                                cws.crawl_time = es_crawl_time
                                cws.web_status = '200'
                                cws.save()
                                print(url, source, interval, es_crawl_time)

                        else:
                            cws = CrawlWarning(status='0', warn_time=today, crawl_id=crawler_id,
                                               crawler_name=crawler_name, crawl_time=es_crawl_time)

                            cws.save()

                    else:
                        if cws:
                            cws = cws[0]
                            if cws.status == '0':
                                cws.web_status = '200'
                                cws.status = '2'
                                cws.warn_time = today
                                cws.save()

                            elif cws.status == '2':
                                # cws = CrawlWarning(web_status='200', warn_time=today, crawl_id=crawler_id,
                                #                    crawler_name=crawler_name, crawl_time=es_crawl_time)
                                cw.crawl_time = es_crawl_time
                                cw.warn_time = today
                                cw.web_status = '200'
                                cws.save()


                except:
                    pass
# 启动一个方法, 每n天修改数据库的状态
@shared_task
def await_warning_celery(crawler_name):
    cws = CrawlWarning.objects.filter(crawler_name=crawler_name)
    for cw in cws:
        cw.status = 2
        cw.save()

