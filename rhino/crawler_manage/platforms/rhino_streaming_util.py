#coding=utf-8

# Author: Ron Lin
# Date: 2017/9/21
# Email: hdsmtiger@gmail.com

import os, sys, time, subprocess
import shutil
from rhino import settings
import time
from django.db.models.query import QuerySet
from os import listdir
from os.path import isfile

if __name__ != "__main__": #for testing purpose
    from crawler_manage.models import Task

BASE_FOLDER = "/etc/rhino"
CRAWLER_FOLDER = os.path.join(BASE_FOLDER, "crawler_app")
TASK_FOLDER = os.path.join(BASE_FOLDER, "task")
LIB_FOLDER = os.path.join(BASE_FOLDER, "lib")
PID_FILE_NAME = "pid.txt"
#JAR_FILE_NAME = "rhino-streaming.jar"
#JAR_FILE_PATH = os.path.join(LIB_FOLDER, JAR_FILE_NAME)
CONFIG_FILE_NAME = "application.properties"
LOG_FILE_NAME = "streaming.log"
JAVA_MAIN_CLASS = "com.yscredit.rhino.Launch"

STREAMING_JOBS = {}

if len(str(settings.JAVA_HOME).strip()) <= 0:
    JAVA_BIN = 'java'
else:
    JAVA_BIN = str(settings.JAVA_HOME).strip() + "/bin/java"


class RhinoStreamingUtil:

    def __init__(self, server="", port=8000, username="", password=""):
        self.__server = server
        self.__port = port
        self.__username = username
        self.__password = password

    @staticmethod
    def check_status(tasks):
        status = {}
        if isinstance(tasks, list) or isinstance(tasks, QuerySet):
            for task in tasks:
                task_id = task.id
                if hasattr(task, 'clean_method') and task.clean_method == 'common':
                    task.id = task.processor_id
                status[task_id] = RhinoStreamingUtil.check_status_for_single_task(task)
        else:
            raise TypeError("Input parameter is not a list.")
        return status

    @staticmethod
    def check_status_for_single_task(task):
        pid = RhinoStreamingUtil.get_program_pid(task)
        if pid == "":
            return False
        return True

    @staticmethod
    def start_clean_deploy(task):
        #准备工作环境
        RhinoStreamingUtil.__prepare_working_folder(task)

        RhinoStreamingUtil.__start_program(task)
        #STREAMING_JOBS[task.id] = program

    @staticmethod
    def stop_clean_deploy(task):
        pass

    @staticmethod
    def __prepare_working_folder(task):
        task_id = task.id
        if hasattr(task, "crawler_id"):
            crawler_id = task.crawler_id
        else:
            crawler_id = task_id
        # if not os.path.isfile(JAR_FILE_PATH):
        #     raise Exception("Jar file %s is not exists" % JAR_FILE_PATH)
        # 清空任务目录下所有文件
        task_folder = os.path.join(TASK_FOLDER, task_id)
        if os.path.exists(task_folder):
            shutil.rmtree(task_folder)

        # 将爬虫目录的文件拷贝到任务目录
        shutil.copytree(os.path.join(CRAWLER_FOLDER, crawler_id), os.path.join(TASK_FOLDER, task_id))

        # prepare application.properties
        config = open(os.path.join(task_folder, CONFIG_FILE_NAME), "w")
        config.write(RhinoStreamingUtil.populate_task_config_file(task))
        config.close()

    @staticmethod
    def get_program_pid(task):
        config_file_path = os.path.join(TASK_FOLDER, task.id, CONFIG_FILE_NAME)
        result = subprocess.getoutput("ps aux | grep java \
            | grep %s | grep -v grep | awk '{print $2}'" % config_file_path)
        return result

    # @staticmethod
    # def get_daemon_pid(full_app_path):
    #     result = subprocess.getoutput("ps aux | grep python \
    #         | grep '%s monitor' | grep -v grep | awk '{print $2}'" % full_app_path)
    #     return result

    @staticmethod
    def __start_program(task):
        app_lib_path = os.path.join(TASK_FOLDER, task.id)
        b, task_clean_app_filename = os.path.split(task.clean_app)
        clean_app = os.path.join(app_lib_path, task_clean_app_filename)
        log_path = os.path.join(TASK_FOLDER, task.id, LOG_FILE_NAME)
        p_pid = RhinoStreamingUtil.get_program_pid(task)
        config_path = os.path.join(TASK_FOLDER, task.id, CONFIG_FILE_NAME)
        if p_pid != '':
            print('It seems this program is already running...')
        else:
            print('Starting program...')
            # -Xms1024m -Xmx1024m -Xmn256m \
            # 拼接classpath
            #b, task_clean_app = os.path.split(clean_app)
            classpath = clean_app
            for f in listdir(LIB_FOLDER):
                if isfile(os.path.join(LIB_FOLDER, f)):
                    classpath = classpath + ":" + os.path.join(LIB_FOLDER, f)

            cmd = 'nohup %s  -server -Dfile.encoding=UTF-8 -classpath %s  %s \
             %s >> %s 2>&1 &' % (JAVA_BIN, classpath, JAVA_MAIN_CLASS, config_path, log_path)
            print('command is: ' + cmd)
            with open(log_path, 'w') as log_file:
                log_file.write('execute command is: ' + cmd)
            if os.system('nohup %s  -server -Dfile.encoding=UTF-8 -classpath %s  %s \
             %s >> %s 2>&1 &' % (JAVA_BIN, classpath, JAVA_MAIN_CLASS, config_path, log_path)) == 0:
                print('start program successfully and pid is ' + RhinoStreamingUtil.get_program_pid(task))

    # @staticmethod
    # def start_daemon(full_app_path):
    #     d_pid = RhinoStreamingUtil.get_daemon_pid(full_app_path)
    #     if d_pid != '':
    #         print('It seems this daemon is already running...')
    #     else:
    #         print('Starting daemon...')
    #         if os.system('nohup python %s monitor >> log/daemon.log 2>&1 &' % full_app_path) == 0:
    #             print('start daemon successfully and pid is ' + RhinoStreamingUtil.get_daemon_pid(full_app_path))

    @staticmethod
    def stop_program(task):
        p_pid = RhinoStreamingUtil.get_program_pid(task)
        if p_pid == '':
            print('It seems this program is not running...')
        else:
            try_time = 1
            while RhinoStreamingUtil.get_program_pid(task) != '' and try_time < 6:
                os.system('kill ' + p_pid)
                try_time += 1
                time.sleep(1)
            if try_time == 6:
                os.system('kill -9 ' + p_pid)
            print('program stopped')

    @staticmethod
    def populate_task_config_file(task):

        connection_url = settings.ELASTIC_SEARCH_SERVER + ':' + settings.ELASTIC_SEARCH_PORT
        config_file = ''
        config_file += 'connection.url=%s\n' % connection_url
        config_file += 'batch.size=%s\n' % settings.ELASTIC_SEARCH_INSERT_BATCH_SIZE
        config_file += 'max.retries=%s\n' % settings.ELASTIC_SEARCH_INSERT_TRY
        config_file += 'key.ignore=true\n'
        config_file += 'fail.record.type.name=%s\n' % settings.ELASTIC_SEARCH_FAIL_TYPE
        config_file += 'fail.record.index.name=%s\n' % settings.ELASTIC_SEARCH_FAIL_INDEX

        config_file += 'topics=%s\n' % task.id
        config_file += 'es.resources=%s\n' % task.deploy_target

        if task.clean_parameters and len(task.clean_parameters) > 0:
            config_file += 'java.process.class=%s\n' % task.clean_parameters

        config_file += 'application.id=%s\n' % task.id

        config_file += 'rhino.server=%s\n' % settings.RHINO_SERVER

        config_file += 'kafka.servers=%s\n' % settings.KAFKA_SERVERS
        config_file += 'schema.register.server=%s\n' % settings.KAFKA_SCHEMA_REGISTER_SERVER

        return config_file
    # @staticmethod
    # def stop_daemon(full_app_path):
    #     d_pid = RhinoStreamingUtil.get_daemon_pid(full_app_path)
    #     if d_pid == '':
    #         print('It seems daemon is not running...')
    #     else:
    #         os.system('kill ' + d_pid)
    #         print('daemon stopped')

if __name__ == "__main__":
    # class Task:
    #     id = 'test_whole_process_0'
    #     name = 'hello'
    #     crawler_id = 'test_whole_process'
    #     deploy_target = 'aaa/bbb,ccc/ddd'
    #     clean_parameters = 'com.yscredit.rhino.Launch'
    #rhino_streaming = RhinoStreamingUtil
    #task = Task
    #RhinoStreamingUtil.prepare_working_folder(task)
    pass