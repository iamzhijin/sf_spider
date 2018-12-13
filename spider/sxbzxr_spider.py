import threading
import json
import requests
import queue
import time
from mysqldb.DBUtil import MysqlPoll


root_url = "http://134.175.168.147/ssfwapi/ssfw_app/app/bgt"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
}
data = {
    "cid": "C_JRSFW",
    "fydm": 350504,
    "slfy": 3505,
    "pagerows": 20,
}


class ThreadCrawl(threading.Thread):
    def __init__(self, crawl_thread, page_queue, data_queue):
        super(ThreadCrawl, self).__init__()
        self.crawl_thread = crawl_thread
        self.page_queue = page_queue
        self.data_queue = data_queue

    def run(self):
        print('%s start' % self.crawl_thread)
        while not CRAWL_EXIT:
            try:
                page = self.page_queue.get(block=False)
                data['postion'] = page
                response = requests.post(url=root_url, headers=headers, data=data)
                response = response.json()
                self.data_queue.put(response)
                time.sleep(0.7)
            except Exception as e:
                print(e) 
        print('%s end' % self.crawl_thread)           



class ParseData(threading.Thread):
    def __init__(self, parse_thread, data_queue):
        super(ParseData, self).__init__()
        self.parse_thread = parse_thread
        self.data_queue = data_queue 

    def run(self):
        while not PARSE_EXIT:
            try:
                data = self.data_queue.get(block=False) 
                self.save_data(data) 
            except Exception as e:
                print(e)

    def save_data(self, data):
        data = data['data'] 
        for each_sx in data:
            item = {}
            item['name'] = each_sx['xm']
            item['fr'] = each_sx['frxm']
            item['certificate'] = each_sx['zjzl']
            item['credti_num'] = str(each_sx['zjhm'])
            item['case_on'] = each_sx['ah']
            item['court'] = each_sx['fymc']
            item['lose_status'] = each_sx['sxzt']
            item['basis_case'] = each_sx['zxyjwh']
            item['perform_status'] = each_sx['bzxrlxqr']
            item['detail'] = each_sx['bzxrjtqx']
            item['publish_date'] = each_sx['fbsj']

            keys = ','.join(item.keys())
            values = ','.join(list(map(lambda x: "'%s'" % x, item.values())))
            sql = "INSERT INTO sxbzxr (%s)VALUES(%s)" % (keys, values)
            MysqlPoll().insert(sql)
            print('===============success=============')


def get_total_page(root_url, headers, data):
    '''
        get the total page for page queue
    '''
    data['postion'] = 1
    total_page = 0
    response = requests.post(url=root_url, headers=headers, data=data)
    if response.status_code == 200:
        response = response.json()
        total_count = int(response['count'])
        total_page = total_count / data['pagerows']
        if total_count % data['pagerows'] > 0:
            total_page += 1
    return total_page    


CRAWL_EXIT = False
PARSE_EXIT = False

def main():
    '''
    control the threads crawl
    '''    
    total_page = get_total_page(root_url, headers, data)

    # 创建页面队列
    page_queue = queue.Queue(total_page)
    for page in range(1, 3):
        page_queue.put(page)
    # 创建采集结果队列
    data_queue = queue.Queue() 
    lock = threading.Lock()

    # 创建页面抓取进程
    thread_crawl = []
    crawl_list = ['thread_crawl_1', 'thread_crawl_2', 'thread_crawl_3']
    for crawl_thread in crawl_list:
        thread = ThreadCrawl(crawl_thread, page_queue, data_queue) 
        thread.start()
        thread_crawl.append(thread)

    # 创建页面解析进程
    thread_parse = []
    parse_list = ['thread_parse__1', 'thread_parse__2', 'thread_parse__3'] 
    for parse_thread in parse_list:
        thread = ParseData(parse_thread, data_queue) 
        thread.start()
        thread_parse.append(thread)    

    # 当页面队列不为空时 保持线程循环
    while not page_queue.empty():
        pass
    global CRAWL_EXIT    
    CRAWL_EXIT = True
    print("page queue is empty")    

    for thread in thread_crawl:
        thread.join()

    # 当解析队列不为空时 保持线程循环
    while not data_queue.empty():
        pass
    global PARSE_EXIT
    PARSE_EXIT = True
    print("data queue is empty")

    for thread in thread_parse:
        thread.join()      
    

if __name__ == "__main__":
    main()    
