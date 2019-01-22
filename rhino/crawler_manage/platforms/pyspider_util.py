# coding=utf-8

# Author: Ron Lin
# Date: 2017/9/20
# Email: hdsmtiger@gmail.com

# Desc: pyspider 工具类
import requests
import time
import json

# pyspide 任务名生成
def compose_pyspider_task_name(task_id, project_code, crawler_code):
    return project_code + '|' + crawler_code + '|' + task_id


class PyspiderUtil:

    # 类初始化
    # server: pyspider服务器地址
    # port: 端口
    # username: 用户名
    # password: 密码
    def __init__(self, server, port, username='', password=''):
        self.__server = "http://" + server.replace("http://", "")
        self.__port = port
        self.__username = username
        self.__password = password

    def login(self):
        pass

    # 提交代码到pyspider平台，并使用task_name作为任务名
    def submit_task(self, pyspider_code, task_name):
        url = '{}:{}/debug/{}/save'.format(self.__server, self.__port, task_name)
        data = {'script': pyspider_code}
        page = requests.post(url, data=data)
        return True if page.text == 'ok' else False

    def update_burst(self, task_name, task_rate):
        url = '{}:{}/update'.format(self.__server, self.__port)
        data = {
            'name': 'rate',
            'value': task_rate,
            'pk': task_name
        }
        page = requests.post(url, data=data)
        return True if page.text == 'ok' else False

    def update_task(self, task_name, task_status):
        url = '{}:{}/update'.format(self.__server, self.__port)
        data = {
            'name': 'status',
            'value': task_status,
            'pk': task_name
        }
        page = requests.post(url, data=data)
        return True if page.text == 'ok' else False

    def delete_task(self, task_name):
        self.update_task(task_name, 'STOP')
        url = '{}:{}/update'.format(self.__server, self.__port)
        data = {
            'name': 'group',
            'value': 'delete',
            'pk': task_name
        }
        page = requests.post(url, data=data)
        return True if page.text == 'ok' else False

    # 在pyspider平台上查看任务task_name的运行状态
    # 返回 0： 停止， 1：暂停， 2：运行, 3：状态未知（如pyspider服务器没有响应）,4没有这个project
    def check_status(self, task_name):
        url = '{}:{}/status/{}'.format(self.__server, self.__port, task_name)
        status = requests.get(url)
        if status.text == 'RUNNING':
            return 2
        elif status.text == 'NONE':
            return 4

        return 0


    # 启动任务
    # 返回 true：成功， false：失败
    def start_task(self, task_name, task_rate=None):
        status = self.check_status(task_name)
        if status == 4:
            return False
        self.update_task(task_name, 'RUNNING')
        time.sleep(2)
        self.update_burst(task_name, task_rate)
        time.sleep(2)
        url = '{}:{}/run'.format(self.__server, self.__port)
        data = {'project': task_name}
        page = requests.post(url, data=data)
        rst = json.loads(page.text).get('result')
        return True if rst else False

    # 停止任务
    # 返回 true：成功， false：失败
    def stop_task(self, task_name):
        return self.update_task(task_name, 'STOP')



    # 暂停任务
    # 返回 true：成功， false：失败
    def pause_task(self, task_name):
        pass



if __name__ == '__main__':
    a = """#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-09-20 16:51:15
# Project: baidu

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.baidu.com', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }
    """
    ps = PyspiderUtil('http://10.1.2.139', '5000')
    print(ps.submit_task(a, 'test'))
    # print(ps.start_task('test'))
    # print(ps.check_status('aaa'))
    # print(ps.stop_task('test'))
