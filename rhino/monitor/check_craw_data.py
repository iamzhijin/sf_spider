#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime

import pymysql,pymongo
import traceback,logging
import re,json


def getData_Mysql():
    try:
        conn = pymysql.connect(host = '10.1.1.25',db = 'rhino',user = 'rhino',password = 'rhino',charset='utf8', use_unicode=True)
        cursor = conn.cursor()
        sql = "SELECT ent_name,province,content FROM monitor_crawdatainfo "
        cursor.execute(sql)
        conn.commit()
        results = cursor.fetchall()
        return results
    except Exception as e:
        logging.warn(traceback.format_exc())


def getData_Mongo(necredit,entName,province):
    """
        获取monggo数据
    :param entName: 企业名
    :return:
    """
    cur = necredit.find({'catEntName': entName,'province':province}).sort("input_time",pymongo.DESCENDING)
    for res in cur:
        return res
def format_mongo_basicList(res_mongo,list_basicList_mongo):
    try:
        if 'gsgsdjxx' in res_mongo.keys() and res_mongo['gsgsdjxx'] :

            if '登记信息' in res_mongo['gsgsdjxx'].keys() and res_mongo['gsgsdjxx']['登记信息']:

                if '基本信息' in res_mongo['gsgsdjxx']['登记信息'].keys() and res_mongo['gsgsdjxx']['登记信息']['基本信息']:
                    list_basicList_mongo.append(res_mongo['gsgsdjxx']['登记信息']['基本信息'])
    except Exception:
        logging.warn(traceback.format_exc())
    return list_basicList_mongo

def format_mongo_shareHolderList(res_mongo,list_shareHolderList_mongo):
    """
        格式化股东信息
    :param res_mongo: mongo查询结果
    :param list_shareHolderList_mongo:
    :return:
    """
    try:
        if 'gsgsdjxx' in res_mongo.keys() and res_mongo['gsgsdjxx'] :

            if '登记信息' in res_mongo['gsgsdjxx'].keys() and res_mongo['gsgsdjxx']['登记信息']:

                if '股东信息' in res_mongo['gsgsdjxx']['登记信息'].keys() and res_mongo['gsgsdjxx']['登记信息']['股东信息']:

                    if 'datalist' in res_mongo['gsgsdjxx']['登记信息']['股东信息'] and res_mongo['gsgsdjxx']['登记信息']['股东信息']['datalist']:

                        for shareHolder_info in res_mongo['gsgsdjxx']['登记信息']['股东信息']['datalist']:
                            dict_shareHolder = {}
                            for key in shareHolder_info.keys():
                                if key =='详情':
                                    continue
                                dict_shareHolder[key] =shareHolder_info[key]
                            list_shareHolderList_mongo.append(dict_shareHolder)
    except Exception:
        logging.warn(traceback.format_exc())

    return list_shareHolderList_mongo

def format_mongo_personList(res_mongo,list_personList_mongo):


    try:
        if 'gsgsbaxx' in res_mongo.keys() and res_mongo['gsgsbaxx'] :

            if '备案信息' in res_mongo['gsgsbaxx'].keys() and res_mongo['gsgsbaxx']['备案信息']:

                if '主要人员信息' in res_mongo['gsgsbaxx']['备案信息'].keys() and res_mongo['gsgsbaxx']['备案信息']['主要人员信息']:

                     if 'datalist' in res_mongo['gsgsbaxx']['备案信息']['主要人员信息'] and res_mongo['gsgsbaxx']['备案信息']['主要人员信息']['datalist']:

                         list_personList_mongo =res_mongo['gsgsbaxx']['备案信息']['主要人员信息']['datalist']
    except Exception:
        logging.warn(traceback.format_exc())
    return list_personList_mongo

def format_mongo_alterList(res_mongo,list_alterList_mongo):
    try:
        if 'gsgsdjxx' in res_mongo.keys() and res_mongo['gsgsdjxx'] :

            if '登记信息' in res_mongo['gsgsdjxx'].keys() and res_mongo['gsgsdjxx']['登记信息']:

                if '变更信息' in res_mongo['gsgsdjxx']['登记信息'].keys() and res_mongo['gsgsdjxx']['登记信息']['变更信息']:

                     if 'datalist' in res_mongo['gsgsdjxx']['登记信息']['变更信息'] and res_mongo['gsgsdjxx']['登记信息']['变更信息']['datalist']:

                        list_alterList_mongo= res_mongo['gsgsdjxx']['登记信息']['变更信息']['datalist']

    except Exception:
        logging.warn(traceback.format_exc())
    return list_alterList_mongo


def cmp_mysql2mongo_basicList(mysql_basic,mongo_basic):
    """
        基本信息比较
    :param mysql_basic:公示系统数据
    :param mongo_basic:mongo数据
    :return:
    """
    flag =True
    try:
        for mysql_item in mysql_basic[0].keys():
            for mongo_item in mongo_basic[0].keys():
                if mysql_item ==mongo_item:
                    mysql_value = mysql_basic[0][mysql_item]
                    mongo_value = mongo_basic[0][mongo_item]
                    if mysql_value !=mongo_value:
                        flag=False
                        logging.warn("基本信息-{},公示系统:{},mongo:{}".format(mysql_item,mysql_value,mongo_value))
    except Exception:
        logging.warn(traceback.format_exc())
        flag =False
    return flag

def cmp_mysql2mongo_shareHolderList(gsxt_shareHolderList,formatted_mongo_shareHolderList):

    flag = True
    if not gsxt_shareHolderList and not formatted_mongo_shareHolderList :
        return flag
    if gsxt_shareHolderList and not formatted_mongo_shareHolderList :
        flag =False
        logging.warn("股东信息，公示系统：有，mongo：无")
        return flag
    if not gsxt_shareHolderList and formatted_mongo_shareHolderList :
        flag =False
        logging.warn("股东信息，公示系统：无，mongo：有")
        return flag
    # 数量
    if len(gsxt_shareHolderList)!=len(formatted_mongo_shareHolderList):
        flag = False
        logging.warn("股东数量不一致：公示系统：{}个，mongo:{}个".format(len(gsxt_shareHolderList),len(formatted_mongo_shareHolderList)))
        return flag
    try:
        for gsxt_shareHolder_info in gsxt_shareHolderList:
            for mongo_shareHolder_info in formatted_mongo_shareHolderList:
                if gsxt_shareHolder_info['序号'] ==mongo_shareHolder_info['序号']:
                    for item in gsxt_shareHolder_info:
                        if gsxt_shareHolder_info[item] != mongo_shareHolder_info[item]:
                            flag = False
                            logging.warn("股东信息：序号:{}，{},公示系统:{},mongo:{}".format(gsxt_shareHolder_info['序号'],item,gsxt_shareHolder_info[item],mongo_shareHolder_info[item]))


    except Exception:
        logging.warn(traceback.format_exc())
        flag =False

    return flag

def rm_same(lst1,lst2):
    for l1 in lst1:
        for l2 in lst2:
            if l1 == l2:
                lst1.remove(l1)
                lst2.remove(l2)
                if not lst1 or not lst2:
                    return
                rm_same(lst1,lst2)

def cmp_mysql2mongo_personList(gsxt_personList,formatted_mongo_personList):

    flag = True
    if not gsxt_personList and not formatted_mongo_personList :
        return flag
    if gsxt_personList and not  formatted_mongo_personList :
        flag =False
        logging.warn("主要人员信息，公示系统：有，mongo：无")
        return flag
    if not gsxt_personList and  formatted_mongo_personList :
        flag =False
        logging.warn("主要人员信息，公示系统：无，mongo：有")
        return flag
    if len(gsxt_personList)!=len(formatted_mongo_personList):
        flag = False
        logging.warn("主要人员数量不一致：公示系统：{}个，mongo:{}个".format(len(gsxt_personList),len(formatted_mongo_personList)))
        return flag
    try:
        # remove相同的
        rm_same(gsxt_personList,formatted_mongo_personList)

        if gsxt_personList or formatted_mongo_personList :
            flag=False
            logging.warn("主要人员信息,公示系统:{},mongo:{}".format(gsxt_personList,formatted_mongo_personList))
    except Exception:
        logging.warn(traceback.format_exc())
        flag =False
    return flag

def cmp_mysql2mongo_alterList(gsxt_alterList,formatted_mongo_alterList):
    flag = True
    if not gsxt_alterList and not formatted_mongo_alterList :
        return flag
    if gsxt_alterList and not  formatted_mongo_alterList :
        flag =False
        logging.warn("变更信息，公示系统：有，mongo：无")
        return flag
    if not gsxt_alterList and  formatted_mongo_alterList :
        flag =False
        logging.warn("变更信息，公示系统：无，mongo：有")
        return flag

    if len(gsxt_alterList)!=len(formatted_mongo_alterList):
        flag = False
        logging.warn("变更数量不一致：公示系统：{}个，mongo:{}个".format(len(gsxt_alterList),len(formatted_mongo_alterList)))
        return flag
    try:
        for gsxt_alter_info in gsxt_alterList:
            for mongo_alter_info in formatted_mongo_alterList:
                if gsxt_alter_info['序号'] ==mongo_alter_info['序号']:
                    for item in gsxt_alter_info:
                        gsxt_value = gsxt_alter_info[item].strip()
                        mongo_value = mongo_alter_info[item].strip()
                        if gsxt_value != mongo_value:
                            flag = False
                            logging.warn("变更信息：序号:{}，{},公示系统:{},mongo:{}".format(gsxt_alter_info['序号'],item,gsxt_value,mongo_value))

    except Exception:
        logging.warn(traceback.format_exc())
        flag =False
    return flag
if __name__ =='__main__':

    # 初始化
    # 连接mongo [一直开着]
    # 奎爷mongo数据
    mongoconn1 = pymongo.MongoClient('59.110.124.36', 10001)
    resdb1 = mongoconn1.resdb  # choose database
    resdb1.authenticate("ysmongor", "ysmongor")
    necredit = resdb1.necredit  # choose table


    global ent_count,rich_count,poor_count
    ent_count = 0
    rich_count = 0
    poor_count = 0
    error_entName_list = []

    # 连接mysql 获取公示系统数据(连接一次 获取所有企业信息)
    results = getData_Mysql()
    for result in results:
        entName = result[0]
        province = result[1]
        print(entName,province)
        content_mysql = result[2]
        content_mysql = json.loads(content_mysql)


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

        res_mongo = getData_Mongo(necredit,entName)
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
            rich_count +=1
        else:
            poor_count +=1
        ent_count +=1
    scope = "当前批量测试覆盖范围：基本信息，股东信息，主要人员信息，变更信息 \n"
    sum_count = "当前测试总企业数量：%s \n"%ent_count
    correct_count = "完全正确：%s \n"%rich_count
    error_count = "有错误的：%s \n"%poor_count
    error_entName = "发生错误的企业："

    if error_entName_list:
        count =0
        for entName in error_entName_list:
            count +=1
            error_entName = error_entName +entName+"\n"
            if count == len(error_entName_list):
                error_entName = error_entName
    else:
        error_entName = error_entName + "无"

    text = scope+sum_count+correct_count+error_count+error_entName
    print(text)
