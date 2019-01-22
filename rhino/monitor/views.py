from django.shortcuts import render
from django.http import *
from django.template import RequestContext,loader
from .serializer import CrawDataInfoSerializer
from rest_framework.response import Response
from .models import *
from rest_framework.decorators import api_view
import time,requests,traceback,pymongo
from requests.adapters import HTTPAdapter
from .check_craw_data import *
from crawler_manage.models import Crawler
from crawler_manage.models import Project
from crawler_manage.models import Task
from crawler_manage.models import Processor
from crawler_manage.models import TaskServer
from crawler_manage.models import SpiderServer
from crawler_manage.models import SpiderTask
from .models import CrawlWarning
from .es_search import EsMan
import requests
# 邮件
import smtplib,os,shutil
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE,formatdate
from email import encoders
import threading
import datetime
# 模拟登录
from selenium import webdriver
from selenium.webdriver.support.ui import Select

from datetime import datetime
from datetime import date
from datetime import timedelta
from concurrent import futures
from rest_framework.response import Response
from crawler_manage.serializer import CrawlerSerializer
import pytz
from .serializer import CrawlWarningSerializer
from .tasks import celery_fetcher
from .tasks import await_warning_celery
from crawler_manage.platforms.pyspider_util import compose_pyspider_task_name
from rhino.settings import PYSPIDER_DATABASE_HOST
from rhino.settings import PYSPIDER_DATABASE_NAME
from rhino.settings import PYSPIDER_DATABASE_PASSWORD
from rhino.settings import PYSPIDER_DATABASE_USERNAME
from rhino.settings import PYSPIDER_DATABASE_PORT
from .MysqlBase import MysqlBase
import logging
from pytz import timezone
from crawler_manage.platforms.pyspider_util import PyspiderUtil
logger = logging.getLogger(__name__)

#线程初始化
thread_test=""




# 接收监控创建表单提交请求
def add_monitor(request):
    # 玩一玩
    content ={}
    if request.POST:
        monitor_province = request.POST['monitor_province']
        monitor_entName = request.POST['monitor_entName']
        monitor_content = request.POST['monitor_content']
        # 存到mysql中
        CrawDataInfo.objects.create(province=monitor_province,ent_name=monitor_entName,content=monitor_content)
    return render(request, "html/add_monitor.html", content)

#测试结果
def crawData_check_result(request):
    today = time.strftime("%Y-%m-%d", time.localtime())
    testResultInfo = TestResultInfo.objects.filter(create_time__gte=today).order_by('-create_time')
    if not testResultInfo:
        content = {
            "result":"今天还未进行测试"
        }
    else:
        testResultInfo = testResultInfo[0]
        content = {
            "title":str(today)+"测试报告",
            "test_count":testResultInfo.test_count,
            "correct_count":testResultInfo.correct_count,
            "error_count":testResultInfo.error_count,
            "error_entName":testResultInfo.error_entName,
            "create_time":testResultInfo.create_time
        }
    return render(request,'html/crawData_check_result.html',content)

# 监控列表
def monitor_list(request):

    crawDataInfo_list = CrawDataInfo.objects.all()
    list2 = []
    size = crawDataInfo_list.count()
    for crawDataInfo in crawDataInfo_list:
        id = crawDataInfo.id
        province = crawDataInfo.province
        ent_name = crawDataInfo.ent_name
        update_time = crawDataInfo.update_time
        crawDataInfo_dict = {
            'id':id,
            'province':province,
            'ent_name':ent_name,
            'update_time':update_time
        }
        list2.append(crawDataInfo_dict)
    content = {
        'data':list2,
        'size':size
    }
    return render(request,'html/monitor_list.html',content)

# 删除按钮
@api_view(['POST'])
def deleteCrawDataInfo(request):
    entName = request.POST['sel_entName[0][ent_name]']
    c = CrawDataInfo.objects.get(ent_name=entName)
    c.delete()
    # return 1
    return render(request,'html/monitor_list.html')

# 监控列表加载数据
@api_view(['POST'])
def monitor_list_api(request):
    limit = request.POST.get('limit')
    offset = request.POST.get('offset')
    crawDataInfoList = CrawDataInfo.objects.all()
    size = crawDataInfoList.count()
    if limit and limit == '-1':
        data = crawDataInfoList[int(offset):]
    else:
        data = crawDataInfoList[int(offset):int(offset) + int(limit)]
    crawler_ser = CrawDataInfoSerializer(data, many=True)
    return Response({"data": crawler_ser.data,"size":size})

# 跳转启动监控页面,并且监控当前线程
def start_monitorHTML(request):
    content={}
    Thread_name_list= []
    for thread in threading.enumerate():
        Thread_name_list.append(thread.getName())
    print(Thread_name_list)
    if "Thread-test" in Thread_name_list:
        content = {"buttonName":"停止监控"}
    else:
        content = {"buttonName":"启动监控"}
    return render(request,'html/start_monitor.html',content)


# 启动监控
def lanch_monitor(request):
    # 开启监控线程
    thread_obj_list = threading.enumerate()
    Thread_name_list =[]
    for thread in thread_obj_list:
        Thread_name_list.append(thread.getName())
    # 启动监控
    if "Thread-test" not in Thread_name_list :
        thread_test = monitor_thread(name="Thread-test")
        thread_test.start()

        if not thread_test.is_alive():
            return render(request,'html/start_monitor.html')
        else:
            start_monitorHTML(request)
            return render(request,'html/crawData_check_result.html')
    else:
        # 停止监控
        stop_monitor(request)

# 对比测试
def lanch_cmp(request):
    CrawDataInfo_list = CrawDataInfo.objects.all()
    # 开始测试
    check_crawData(CrawDataInfo_list)


    return render(request, 'html/crawData_check_result.html')

# 关闭监控
def stop_monitor(request):
    thread_obj_list = threading.enumerate()
    for thread_obj in thread_obj_list:
        threadName = thread_obj.getName()
        if "Thread-test" == threadName:
            thread_obj.stop()
            break
    Thread_name_list =[]
    time.sleep(1)
    for thread in threading.enumerate():
        Thread_name_list.append(thread.getName())
    return render(request,'html/start_monitor.html')
# 开始监控
def do_monitor():
    # 首先触发爬虫
    CrawDataInfo_list = CrawDataInfo.objects.all()

    for crawDataInfo in CrawDataInfo_list:
        entName = crawDataInfo.ent_name
        province = crawDataInfo.province
        print(province,entName)
        # 触发
        print("触发爬虫：begin")
        taggle_crawler(entName,province)
        print("触发爬虫：end")
        time.sleep(6)

    print("触发爬虫结束，休息10分钟")
    # # 等待爬虫爬取内容15分钟
    time.sleep(60*15)

    # 开始测试
    check_crawData(CrawDataInfo_list)
    #     dict_res = {
    #     "sum_count":sum_count,
    #     "correct_count":correct_count,
    #     "error_count":error_count,
    #     "error_entName":error_entName
    # }

# 触发爬虫：爬取数据 ，存入mongo
def taggle_crawler(entName,province):
    """
        触发爬虫
    :param entName:
    :param province:
    :return:
    """

    driver = webdriver.PhantomJS(executable_path="phantomjs")
    try:
        driver.get("http://59.110.170.115:7575")
        time.sleep(1)
        # 输入账号密码
        driver.find_element_by_name("user").send_keys("YS")
        driver.find_element_by_name("password").send_keys("YscrediT@808")
        # 模拟点击登录
        driver.find_element_by_xpath("//input[@class='btn btn-default']").click()
        # 等待1秒
        time.sleep(1)
        # post页面
        driver.find_element_by_name("entName").send_keys(entName)
        driver.find_element_by_name("province").send_keys(province)

        s1 = Select(driver.find_element_by_name("topic"))
        s1.select_by_value("PRIOR_CRAW_REQUEST:api_yscredit")

        driver.find_element_by_xpath("//input[@type='submit']").click()

    except Exception :
        print(traceback.format_exc())
    driver.quit()

# 测试爬虫数据：公示系统和mongo对比
def check_crawData(CrawDataInfo_list):

    global ent_count,rich_count,poor_count,mongoconn1,necredit
    ent_count =0
    rich_count =0
    poor_count =0
    error_entName_list = []
    #日期
    today = datetime.date.today()
    # 日志路径名
    logpath = "LOG\\" +str(today)

    # 创建日志目录
    if os.path.exists(logpath):
        shutil.rmtree(logpath)
        os.makedirs(logpath)
    else:
        os.makedirs(logpath)

    logfilename =  logpath + "\\"+str(today)+"_log.log"
    # logger配置
    # 1.create logger
    logging.basicConfig(
        level=logging.WARN,
        format='%(asctime)s\t%(message)s',
                datefmt = '%a, %d %b %Y %H:%M:%S',
                filename=logfilename,
                filemode='w'
    )

    console = logging.StreamHandler()
    console.setLevel(logging.WARN)
    formatter = logging.Formatter('%(asctime)s \t %(message)s')
    console.setFormatter(formatter)

    logging.getLogger().addHandler(console)
    # 连接mysql 获取公示系统数据(连接一次 获取所有企业信息)
    # 生成企业名单
    entName_file_path =  logpath + "\\"+str(today)+"_entName.txt"
    entName_file = open(entName_file_path,'a',encoding='utf-8')
    # 初始化mongo
    # 连接mongo [一直开着]
    # 奎爷mongo数据
    try:
        mongoconn1 = pymongo.MongoClient('59.110.124.36', 10001)
        resdb1 = mongoconn1.resdb  # choose database
        resdb1.authenticate("ysmongor", "ysmongor")
        necredit = resdb1.necredit  # choose table
    except Exception:
        logging.warn("mongo连接不上了")
        logging.shutdown()
        # mongoconn1.close_cursor()
        mongoconn1.close()

    for crawDataInfo in CrawDataInfo_list:

        entName = crawDataInfo.ent_name
        province = crawDataInfo.province
        content_mysql = crawDataInfo.content
        try:
            content_mysql = json.loads(content_mysql)
        except:
            logging.warn(traceback.format_exc())

        entName_file.write(province+"\t"+entName+"\n")
        logging.warn("=====================")
        logging.warn(entName)

        list_basicList_gsxt = []
        list_shareHolderList_gsxt = []
        list_personList_gsxt = []
        list_alterList_gsxt = []
        # 处理mysql数据

        formatted_gsxt_basicList = format_mongo_basicList(content_mysql,list_basicList_gsxt)
        formatted_gsxt_shareHolderList = format_mongo_shareHolderList(content_mysql,list_shareHolderList_gsxt)
        formatted_gsxt_personList = format_mongo_personList(content_mysql,list_personList_gsxt)
        formatted_gsxt_alterList = format_mongo_alterList(content_mysql,list_alterList_gsxt)
        # 格式化mongo数据
        list_basicList_mongo = []
        list_shareHolderList_mongo = []
        list_personList_mongo = []
        list_alterList_mongo = []

        res_mongo = getData_Mongo(necredit,entName,province)
        formatted_mongo_basicList = format_mongo_basicList(res_mongo,list_basicList_mongo)
        formatted_mongo_shareHolderList = format_mongo_shareHolderList(res_mongo,list_shareHolderList_mongo)
        formatted_mongo_personList = format_mongo_personList(res_mongo,list_personList_mongo)
        formatted_mongo_alterList = format_mongo_alterList(res_mongo,list_alterList_mongo)

        results_basic = cmp_mysql2mongo_basicList(formatted_gsxt_basicList,formatted_mongo_basicList)
        results_shareHolder = cmp_mysql2mongo_shareHolderList(formatted_gsxt_shareHolderList,formatted_mongo_shareHolderList)
        results_person = cmp_mysql2mongo_personList(formatted_gsxt_personList,formatted_mongo_personList)
        results_alter = cmp_mysql2mongo_alterList(formatted_gsxt_alterList,formatted_mongo_alterList)

        if results_basic ==True and results_shareHolder==True and results_person==True and results_alter==True :
            flag=True
        else:
            flag=False
            error_entName_list.append(entName)
        # 计数

        if flag:
            rich_count+=1
        else:
            poor_count +=1
        ent_count +=1

    logging.shutdown()
    mongoconn1.close()
    entName_file.close()
     # 邮件参数初始化
    server = {'name':'smtp.yscredit.com',
          'user':'automail@yscredit.com',
          'passwd':'y8svUoBf'}
    fro = 'automail@yscredit.com'
    to = ['46691235@qq.com','haoran@yscredit.com']
    subject = str(today)+"_爬虫数据质量测试报告"
    file_name = entName_file_path
    file_log =logfilename
    files = [file_name,file_log]

    scope = "当前批量测试覆盖范围：基本信息，股东信息，主要人员信息，变更信息 \n"
    sum_count = "当前测试总企业数量：%s \n"%ent_count
    correct_count = "完全正确：%s \n"%rich_count
    error_count = "有错误的：%s \n"%poor_count
    error_entName = ""

    if error_entName_list:
        count =0
        for entName in error_entName_list:
            count +=1
            error_entName = error_entName +entName+","+"\n"
            if count == len(error_entName_list):
                error_entName = error_entName
    else:
        error_entName = error_entName + "无"

    text = scope+sum_count+correct_count+error_count+error_entName

    send_mail(server,fro,to,subject,text,files)


    create_time =time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(error_entName,create_time)
    # 将结果存入mysql
    TestResultInfo.objects.create(
        test_count = ent_count,
        correct_count = rich_count,
        error_count = poor_count,
        error_entName = error_entName,
        create_time =time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    )


# 发送测试结果email
def send_mail(server, fro, to, subject="", text="", files=[]):

    assert type(server) == dict
    assert type(to) == list
    assert type(files) == list

    msg = MIMEMultipart()
    msg['From'] = fro                # 邮件的发件人
    msg['Subject'] = subject         # 邮件的主题
    msg['To'] = COMMASPACE.join(to)  # COMMASPACE==', ' 收件人可以是多个，to是一个列表
    msg['Date'] = formatdate(localtime=True) # 发送时间，当不设定时，用outlook收邮件会不显示日期，QQ网页邮箱会显示日期
    # MIMIMEText有三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码，二和三可以省略不写
    msg.attach(MIMEText(text,'plain','utf-8'))
    try:
        for file in files:          # 添加附件可以是多个，files是一个列表，可以为空
            part = MIMEBase('application', 'octet-stream') #'octet-stream': binary data
            with open(file,'rb') as f:
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
            msg.attach(part)

        smtp = smtplib.SMTP()
        # smtp = smtplib.SMTP_SSL()  # 使用SSL的方式去登录(例如QQ邮箱，端口是465)
        smtp.connect(server['name']) # connect有两个参数，第一个为邮件服务器，第二个为端口，默认是25
        smtp.login(server['user'], server['passwd']) # 用户名，密码
        smtp.sendmail(fro, to, msg.as_string()) # 发件人，收件人，发送信息
        smtp.close()  # 关闭连接
    except Exception:
        logging.warn(traceback.format_exc())

class monitor_thread(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)
        self.name = name
        self.stop_flag = False
    def run(self):
        do_monitor()

    def stop(self):
        self.stop_flag = True

# 定时任务
def cron():
    # 首先触发爬虫
    CrawDataInfo_list = CrawDataInfo.objects.all()

    for crawDataInfo in CrawDataInfo_list:
        entName = crawDataInfo.ent_name
        province = crawDataInfo.province
        print(province,entName)
        # 触发
        taggle_crawler(entName,province)
        time.sleep(6)

    print("触发爬虫结束，休息10分钟")
    # # 等待爬虫爬取内容3个小时
    time.sleep(60*60*3)

    # 开始测试
    # 开始测试
    check_crawData(CrawDataInfo_list)
    #     dict_res = {
    #     "sum_count":sum_count,
    #     "correct_count":correct_count,
    #     "error_count":error_count,
    #     "error_entName":error_entName
    # }

# 大屏显示,跳转
def show_big_screen(request):
    return render(request, 'html/bigscreen_bk.html')







def check_web_status(request):
    # 报警时间间隔



    esman = EsMan()
    # 获得参数
    p_project_name = request.GET.get('project_name')
    p_crawler_name = request.GET.get('crawler_name')
    p_crawl_owner = request.GET.get('crawl_owner')
    status = request.GET.get('status')
    p_limit = request.POST.get('limit', '10')
    p_offset = request.POST.get('offset', '0')

    # 获得请求和上次调试时间差
    # tz = pytz.timezone('Asia/Shanghai')


    params = {'crawl__project_name': p_project_name, 'crawl__crawler_name': p_crawler_name, 'crawl__crawl_owner': p_crawl_owner, 'status': status}
    params = {k: v for k, v in params.items() if v}

    rst = CrawlWarning.objects.select_related('crawl').filter(**params)
    size = CrawlWarning.objects.count()

    # 查询CrawlWarning数据库
    cws = []
    for item in rst:
        crawler_ser = CrawlWarningSerializer(item)
        crawlers_obj = crawler_ser.data

        # 未处理 并且 断更 进行分析; 已经处理直接返回数据内容
        if not item.web_status or int(item.web_status) < 400:
            crawl = item.crawl
            task_id = crawl.processor_id
            project_id = crawl.project_id
            crawl_id = crawl.id
            source = crawl.source

            pyspider_name = compose_pyspider_task_name(task_id=task_id,
                                       project_code=project_id,
                                       crawler_code=crawl_id)

            try:
                print("select status, count(status) as num from `{}` where updatetime>{} group by status ".format(
                        pyspider_name, time.mktime(date.today().timetuple())))
                connector = {
                    'host': PYSPIDER_DATABASE_HOST,
                    'user': PYSPIDER_DATABASE_USERNAME,
                    'password': PYSPIDER_DATABASE_PASSWORD,
                    'db': PYSPIDER_DATABASE_NAME
                }
                pyspider_mb = MysqlBase(connector)
                pyspider = [item for item in pyspider_mb._execute("select status, count(status) as num from `{}` where updatetime>{} group by status ".format(pyspider_name, time.mktime(date.today().timetuple())))]
                crawlers_obj['pyspider'] = pyspider
            except:
                crawlers_obj['pyspider'] = [{'num': 0, 'status': 4}]


            fail_count = esman.agg_fail_record( source)
            crawlers_obj['fail_count'] = fail_count
        cws.append(crawlers_obj)
    obj = {"size": size, "data": cws}

    return JsonResponse(obj)




def project_update_by_day(request):
    project = Project.objects.all()
    es = EsMan()
    today = date.today()
    end = today
    begin = today - timedelta(days=30)
    rst = [{"project_name": item.project_name, "project_count": es.project_all_total(item.es_table), "project_crawl": es.crawled_uncrawled_project(item.es_table), "data": es.agg_day_source(item.es_table, begin=begin, end=end)} for item in project if item.es_table and '/' in item.es_table]

    return JsonResponse(rst, safe=False)


def crawl_total(request):
    crawl_size = Crawler.objects.count()
    project = Project.objects.all()
    es = EsMan()
    crawled_count = sum([es.total(item.es_table) for item in project if item.es_table and '/' in item.es_table])
    return JsonResponse({'crawl_size': crawl_size, 'crawled_count': crawled_count})


def project_all_total(request):
    es = EsMan()
    project = Project.objects.all()
    rst = [{'project_name': item.project_name, 'total': es.project_all_total(item.es_table)} for item in project if item.es_table and '/' in item.es_table]
    return JsonResponse(rst, safe=False)


def crawled_uncrawled_project(request):
    es = EsMan()
    rst = {}
    project = Project.objects.all()
    for item in project :
        if item.es_table and '/' in item.es_table:
            rst = es.crawled_uncrawled_project(item.es_table)
            rst['project_name'] = item.project_name
    return JsonResponse(rst, safe=False)


def crawl_field(request):
    crwal = request.GET.get('crawler_name')


# 点击暂停预警
@api_view(['POST'])
def await_warning(request):
    today = date.today()
    crawler_name = request.POST.get('crawler_name')
    cws = CrawlWarning.objects.filter(crawler_name=crawler_name)
    my_tz = timezone('Asia/Shanghai')
    for cw in cws:
        await_warning_celery.apply_async((crawler_name,), eta=my_tz.localize(datetime.now()) + timedelta(seconds=20))
        cw.warn_time = today
        cw.status = 1
        cw.save()

    return JsonResponse({"code": "0000"})


# 不在预警
@api_view(['POST'])
def no_warning(request):
    today = date.today()
    crawler_name = request.POST.get('crawler_name')
    cws = CrawlWarning.objects.filter(crawler_name=crawler_name)
    for cw in cws:
        cw.warn_time = today
        cw.status = 3
        cw.save()
    return JsonResponse({'code': 0000})


def test_celery(request):
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


                        else:
                            cws = CrawlWarning(status='0', warn_time=today, crawl_id=crawler_id,
                                               crawler_name=crawler_name, crawl_time=es_crawl_time)

                            cws.save()

                    else:
                        if cws:
                            cws = cws[0]
                            if cws.status == '0':
                                cws.web_status = '200'
                                cws.status = '1'
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
    return JsonResponse({'c': '1'})


def test_celery_fetcher(request):
    today = date.today()
    crawlers = Crawler.objects.all()
    for crawler in crawlers:
        crawler_name = crawler.crawler_name
        crawl_id = crawler.id
        if crawler.web_url:
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36'
                }
                response = requests.get(crawler.web_url, headers=headers, timeout=10)
                web_status = response.status_code
            except:
                web_status = 555
            print(crawler.web_url, web_status)
            cws = CrawlWarning.objects.filter(crawler_name=crawler.crawler_name)
            if web_status >= 400:
                if cws:
                    cws = cws[0]
                    if cws.status == '0':
                        cws.web_sestatus = web_status
                        cws.save()

                    elif cws.status == '2':
                        cws.status = '0'
                        cws.warn_time = today
                        cws.web_status = web_status
                        cws.save()

                else:
                    cws = CrawlWarning(status='0', warn_time=today, web_status=web_status, crawl_id=crawl_id,
                                       crawler_name=crawler_name)
                    cws.save()

            else:
                if cws and cws[0].status == '0':
                    cws = cws[0]
                    cws.status = '2'
                    cws.warn_time = today
                    cws.save()
    return JsonResponse({'code': '000'})


def crawler(request):
    crawler_id = request.GET.get('crawler_id')
    es = EsMan()
    try:
        crawler = Crawler.objects.get(pk=crawler_id)
    except:
        return JsonResponse({"code": "0001", "data": "no this crawler"})
    rst = CrawlerSerializer(crawler).data
    project_id = crawler.project_id
    source = crawler.source


    project_crawlers = Crawler.objects.filter(project_id=project_id)
    project_crawlers_counts = [item.count for item in project_crawlers]

    project_crawler_num = len(project_crawlers)
    project_crawler_data_total = sum([int(item) for item in project_crawlers_counts if item])

    projects = Project.objects.filter(code=project_id)[0]
    es_table = projects.es_table
    project_crawled_data_num = es.project_all_total(es_table)

    rst['project'] = {
        "crawler_num": project_crawler_num,
        "crawler_data_total": project_crawler_data_total,
        "crawled_data_num": project_crawled_data_num
    }

    crawl_rst = es.source_today_update(es_table, source)

    rst['crawled_total'] = crawl_rst['crawled_total']
    rst['crawled_update'] = crawl_rst['crawled_update']

    task = Task.objects.filter(crawler_id=crawler.id)[0]
    servers = TaskServer.objects.filter(task=task)

    for server in servers:
        pyspider = PyspiderUtil(server=server.server.host, port=server.server.port)
        try:

            task_id = server.task.id
            if task.clean_method == 'common':
                task_id = server.task.processor_id
            status = pyspider.check_status(compose_pyspider_task_name(task_id=task_id,
                                                                      project_code=server.task.project_id,
                                                                      crawler_code=server.task.crawler_id))
        except:
            status = 0
        if status == 2:
            rst['crawl_status'] = "running"
            break
    else:
        rst['crawl_status'] = "stopping"
    today = date.today()
    end = today
    begin = today - timedelta(days=30)
    rst['data'] = es.agg_day_by_source(es_table, source, begin=begin, end=end)
    return JsonResponse(dict(rst), safe=False)


def field_mapping(request):
    crawler_id = request.GET.get('crawler_id')
    es = EsMan()
    try:
        crawler = Crawler.objects.get(pk=crawler_id)
    except:
        return JsonResponse({"code": "0001", "data": "no this crawler"})
    source = crawler.source
    project_id = crawler.project_id
    projects = Project.objects.filter(code=project_id)[0]
    es_table = projects.es_table
    rst = [item for item in es.mapping(es_table, source)]
    return JsonResponse(rst, safe=False)

@api_view(['POST'])
def update_crawler(request):
    params = request.data
    crawler_id = params['crawler_id']
    crawler = Crawler.objects.get(pk=crawler_id)
    for k in params:
        crawler.k = params[k]
    crawler.save()
    return JsonResponse({'code': 0000})
