from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .form import CrawlForm
from .models import Crawls
from CrawlManager.Util import Util

util = Util()

def CreateCrawl(request):
    '''新建爬虫'''
    if request.method == "POST":
        crawl_form = CrawlForm(request.POST) 
        if crawl_form.is_valid():
            crawl_form_data = crawl_form.clean()
            insert_crawl = Crawls(
                project_id=request.POST['project_id'],
                crawl_name=crawl_form_data['crawl_name'],
                code=crawl_form_data['code'],
                crawl_field=crawl_form_data['crawl_field'],
                source=crawl_form_data['source']
            ) 
            insert_crawl.save()
            return JsonResponse(util.success_result())
        else:
            error_message = crawl_form.errors.as_text()
            return JsonResponse(util.fail_result(data=error_message))    
    else:
        return JsonResponse(util.fail_result(code='002'))


def DeleteCrawl(request):
    '''删除爬虫'''
    pass     


def UpCrawl(request):
    '''更新爬虫'''
    pass


def CrawlList(request):
    '''展示爬虫列表'''
    pass    
