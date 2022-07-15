#coding=utf-8

# Author: Ron Lin
# Date: 2017/9/21
# Email: hdsmtiger@gmail.com

import os
import sys
from setuptools import setup, find_packages

setup(
    name = "rhino",
    version = "0.1",
    packages = find_packages(),
    install_requires = ['ConfigParser==3.5.0',
                        'avro-python3==1.8.2',
                        'certifi==2017.7.27.1',
                        'chardet==3.0.4',
                        'fastavro==0.14.10',
                        'idna==2.6',
                        'requests==2.18.4',
                        'urllib3==1.22',
                        'confluent-kafka==0.11.0',
                        'django-rest-framework==0.1.0',
                        'mysqlclient==1.3.12',
                        'django_crontab==0.7.1',
                        'pymongo==3.5.1',
                        'pymysql==0.7.11',
                        'pygments==2.2.0',
                        'threadpool==1.3.2',
                        'elasticsearch==6.0.0',
                        'celery==4.1.0',
                        'django-celery==3.2.1',
                        'django-celery-results==2.4.0',
                        'xlwt==1.3.0'
                        ],

    author = "Shirong Lin",
    author_email = "hdsmtiger@sina.com",
    url = "http://github.com/hdsmtiger",

)