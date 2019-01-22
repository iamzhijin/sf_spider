#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render
from rest_framework.decorators import api_view
from tempfile import TemporaryFile
from xlwt import Workbook
from elasticsearch import Elasticsearch
import os,sys,datetime,shutil
import zipfile,traceback
from rhino.settings import DEFAULT_FROM_EMAIL,EXPORT_PATH
# 邮件
from django.core.mail import send_mail,BadHeaderError,EmailMessage
import string
import random
import json
import xlrd
from xlutils.copy import copy
# 地址初始化
path = EXPORT_PATH
# 初始化：
cpws_dict = {
    "litigants": 4,
    "title": 5,
    "reasons": 6,
    "court_name": 7,
    "trial_round": 8,
    "source": 9,
    "agents": 10,
    "court_level": 11,
    "trial_date": 12,
    "verdict": 13,
    "content": 14,
    "content_type": 15,
    "type": 16,
    "case_no": 17,
    "court_officers": 18
}

shixin_beizhixing_dict = {
    "name": 0,
    "case_code": 1,
    "age": 2,
    "sex": 3,
    "card_num": 4,
    "business_entity": 5,
    "court_name": 6,
    "area_name": 7,
    "party_type_name": 8,
    "gist_id": 9,
    "reg_date": 10,
    "gist_unit": 11,
    "duty": 12,
    "performance": 13,
    "performed_part": 14,
    "unperform_part": 15,
    "disrupt_type_name": 16,
    "publish_date": 17,
    "source": 18

}
exposure_desk_dict = {
    "release_date": 0,
    "execution_applicant": 1,
    "execute_money": 2,
    "exposure_type": 3,
    "source": 4,
    "address": 5,
    "name": 6,
    "court_name": 7,
    "limiting_cause": 8,
    "case_code": 9,
    "tel_of_court": 10
}
executive_announcement_dict = {
    "name": 0,
    "case_code": 1,
    "address": 2,
    "sex": 3,
    "notice_id": 4,
    "age": 5,
    "execute_money": 6,
    "unexecute_money": 7,
    "itype": 8,
    "court_name": 9,
    "source": 10,
    "case_id": 11,
    "reg_date": 12,
    "card_num": 13,
    "business_entity": 14
}
court_session_announcement_dict = {
    "reason": 1,
    "case_no": 2,
    "court_time": 3,
    "court_room": 4,
    "responding_name": 5,
    "source": 6,
    "undertake_department": 7,
    "content": 8,
    "reason_code_level2": 19,
    "reason_code_level1": 9,
    "reason_code_level4": 12,
    "reason_code_level3": 11,
    "name": 14,
    "reason_code_level5": 13,
    "judge": 15,
    "court_name": 16,
    "court_date": 17,
    "prosecution_name": 18,

}


# 从es中导出企业司法数据
@api_view(['POST'])
def export_ent_sifa_info(request):
    if request.method=='POST':
        # 初始化
        # 线上
        es = Elasticsearch(['10.20.20.105:9200'])
        # 线下
        # es = Elasticsearch(['10.1.1.28:9200'])

        book = Workbook()
        cpws = book.add_sheet("裁判文书",cell_overwrite_ok=True)
        cpws.write(0, 0, "企业名称")
        cpws.write(0, 1, "身份")
        cpws.write(0, 2, "状态")
        cpws.write(0, 3, "其他当事人")
        cpws.write(0, 4, "当事人")
        cpws.write(0, 5, "案件名称")
        cpws.write(0, 6, "案由")
        cpws.write(0, 7, "审理法院")
        cpws.write(0, 8, "审判程序")
        cpws.write(0, 9, "来源")
        cpws.write(0, 10, "代理人")
        cpws.write(0, 11, "法院层级")
        cpws.write(0, 12, "裁判日期")
        cpws.write(0, 13, "判决结果")
        cpws.write(0, 14, "裁判文书内容")
        cpws.write(0, 15, "文书类型")
        cpws.write(0, 16, "案件类型")
        cpws.write(0, 17, "案号")
        cpws.write(0, 18, "法院人员")

        sxbzxr = book.add_sheet("失信被执行人",cell_overwrite_ok=True)
        sxbzxr.write(0, 0, "被执行人姓名/名称")
        sxbzxr.write(0, 1, "案号")
        sxbzxr.write(0, 2, "被执行人年龄")
        sxbzxr.write(0, 3, "被执行人性别")
        sxbzxr.write(0, 4, "证件号码/组织机构代码")
        sxbzxr.write(0, 5, "法定代表人姓名")
        sxbzxr.write(0, 6, "执行法院")
        sxbzxr.write(0, 7, "省份")
        sxbzxr.write(0, 8, "被执行人类型")
        sxbzxr.write(0, 9, "执行依据文书编号")
        sxbzxr.write(0, 10, "立案日期")
        sxbzxr.write(0, 11, "经办机构（做出执行依据单位）")
        sxbzxr.write(0, 12, "生效法律文书确定的义务")
        sxbzxr.write(0, 13, "履行情况")
        sxbzxr.write(0, 14, "已履行部分"),
        sxbzxr.write(0, 15, "未履行部分")
        sxbzxr.write(0, 16, "失信被执行人行为具体情形")
        sxbzxr.write(0, 17, "发布时间")
        sxbzxr.write(0, 18, "来源")

        bgt = book.add_sheet("曝光台",cell_overwrite_ok=True)
        bgt.write(0, 0, "发布/曝光日期")
        bgt.write(0, 1, "申请执行人")
        bgt.write(0, 2, "执行金额")
        bgt.write(0, 3, "曝光类型")
        bgt.write(0, 4, "来源")
        bgt.write(0, 5, "地址")
        bgt.write(0, 6, "被执行人姓名/名称")
        bgt.write(0, 7, "执行法院")
        bgt.write(0, 8, "限制原因")
        bgt.write(0, 9, "案号")
        bgt.write(0, 10, "法院电话")

        bzxr = book.add_sheet("被执行人",cell_overwrite_ok=True)
        bzxr.write(0, 0, "被执行人姓名/名称")
        bzxr.write(0, 1, "案号")
        bzxr.write(0, 2, "地址")
        bzxr.write(0, 3, "被执行人性别")
        bzxr.write(0, 4, "ID")
        bzxr.write(0, 5, "被执行人年龄")
        bzxr.write(0, 6, "执行金额")
        bzxr.write(0, 7, "未执行金额")
        bzxr.write(0, 8, "被执行人类型")
        bzxr.write(0, 9, "执行法院")
        bzxr.write(0, 10, "来源")
        bzxr.write(0, 11, "案件ID")
        bzxr.write(0, 12, "立案日期")
        bzxr.write(0, 13, "证件号码/组织机构代码")
        bzxr.write(0, 14, "法定代表人姓名")

        ktgg = book.add_sheet("开庭公告",cell_overwrite_ok=True)
        ktgg.write(0, 0, "企业名称")
        ktgg.write(0, 1, "案由")
        ktgg.write(0, 2, "案号")
        ktgg.write(0, 3, "开庭时间")
        ktgg.write(0, 4, "法庭")
        ktgg.write(0, 5, "应诉方名字")
        ktgg.write(0, 6, "来源")
        ktgg.write(0, 7, "承办部门")
        ktgg.write(0, 8, "正文")
        ktgg.write(0, 9, "案由编码一级")
        ktgg.write(0, 10, "案由编码二级")
        ktgg.write(0, 11, "案由编码三级")
        ktgg.write(0, 12, "案由编码四级")
        ktgg.write(0, 13, "案由编码五级")
        ktgg.write(0, 14, "当事人姓名")
        ktgg.write(0, 15, "法官")
        ktgg.write(0, 16, "法院")
        ktgg.write(0, 17, "开庭日期")
        ktgg.write(0, 18, "起诉方名字")
        # 日期
        random_str = "".join(random.sample(string.ascii_letters + string.digits, 12))
        today_str = str(datetime.date.today())
        today_random = today_str+random_str
        # 创建目录
        path = os.path.dirname(os.path.realpath(__file__))
        library_path = os.path.join(path, today_random)
        isExists = os.path.exists(library_path)
        if isExists:
            shutil.rmtree(library_path)
            os.mkdir(library_path)
        else:
            os.mkdir(library_path)

        # 导入文件：1，手动导入：2
        export_function = request.POST["export_function"]
        ent_person_name = request.POST["ent_person_name"]
        email_addreass = request.POST["email_addreass"]
        file_export_function = request.FILES.get('file_export_function', None)
        email_addreass_list = []
        # 对email地址处理
        tmp_list = []
        if "," in email_addreass:
            tmp_list = email_addreass.split(",")
            for item in tmp_list:
                if item:
                    email_addreass_list.append(item)
        else:
            email_addreass_list.append(email_addreass)

        ent_person_name_list =[]
        count_dict={
            "cpws_count":1,
            "sxbzxr_count":1,
            "bgt_count":1,
            "bzxr_count":1,
            "ktgg_count":1
        }
        if export_function=="2":
            try:
                ent_person_name_list = ent_person_name.split("\r\n")
            except:
                ent_person_name_list.append(ent_person_name)
            print(ent_person_name_list)
            for entName in ent_person_name_list:
                if entName:
                    # 将数据存入csv文件中,需要concurrency
                    try:
                        export_main_function(es,library_path,entName,cpws,sxbzxr,bgt,bzxr,ktgg,count_dict)
                    except:
                        pass

        else:
            # 读取txt方式
            # 上传文件

            file_path = os.path.join(path, file_export_function.name)
            file_export_function_dest = open(file_path, 'wb+')
            for chunks in file_export_function.chunks():
                file_export_function_dest.write(chunks)
            file_export_function_dest.close()
            # 读取数据进list
            f = open(file_path,'r',encoding="utf-8")
            for line in f:
                entName = line.strip()
                ent_person_name_list.append(entName)
                if entName:
                    # 将数据存入csv文件中,需要concurrency
                    try:
                        export_main_function(es,library_path, entName,cpws,sxbzxr,bgt,bzxr,ktgg,count_dict)
                    except:
                        pass


        # filename = entName + ".csv"
        filename = "企业司法数据.csv"
        # 文件地址
        filename_path = os.path.join(library_path, filename)

        book.save(filename_path)
        book.save(TemporaryFile())
        # 打包
        output_filename = library_path+".zip"
        make_zip(library_path, output_filename)
        print("打包输出地址：%s"%output_filename)
        # 发送email
        subject=today_str+"_导出企业司法数据"
        message = "本次总共导出{}家企业\n".format(len(ent_person_name_list))
        message = message+"\n".join(ent_person_name_list)
        from_email = DEFAULT_FROM_EMAIL
        email = EmailMessage(subject=subject,body=message,from_email=from_email,to=email_addreass_list)
        email.attach_file(output_filename)
        if email.send():
            content = {
                "status": "邮件发送成功"
            }
        else:
            content = {
                "status": "邮件发送失败"
            }

        return render(request, 'html/export_ent_sifa_info.html', content)
# 取数据主逻辑
def export_main_function(es,library_path,entName,cpws,sxbzxr,bgt,bzxr,ktgg,count_dict):


    # 去es各表查询，将结果输出
    es_table_dict = {
        "judge_doc": "total_doc",
        "shixin_beizhixing": "shixin_beizhixing_total",
        "exposure_desk": "exposure_desk",
        "executive_announcement": "executive_announcement_total",
        "court_session_announcement": "court_session_announcement"
    }

    for index, doc_type in es_table_dict.items():
        print(entName,index,doc_type)
        res = getES_search(es, index, doc_type, entName)
        res_list = res["hits"]["hits"]
        handler_excel_multi_files(entName,index,res_list,cpws,sxbzxr,bgt,bzxr,ktgg,count_dict)
        # handler_excel_single_file(entName,index, res_list, book)



@api_view(['GET'])
def go2export_ent_sifa_info(request):
    return render(request,'html/export_ent_sifa_info.html')
# es查询
def getES_search(es, index, doc_type, ent_name):
    query = ""
    if index == "judge_doc":
        query = """
            {
              "query": {
                "nested": {
                  "path": "litigants",
                  "query": {
                    "term": {
                      "litigants.name.keyword": {
                        "value": "%s"
                      }
                    }
                  }
                }

              },"from":0,
              "size":1000
            }
        """ % (ent_name)
    elif index == "court_session_announcement":
        query = """
            {
              "query": {
                "bool": {
                  "must": [
                    {
                      "term": {
                        "name.keyword": "%s"
                      }
                    }
                  ],
                  "must_not": [],
                  "should": []
                }
              },"from":0,
              "size":1000
            }
        """ % (ent_name)
    else:
        query = """
        {
          "query": {
            "term": {
              "name": {
                "value": "%s"
              }
            }
          },"from":0,
              "size":1000
        }
        """ % (ent_name)

    es_result = es.search(
        index=index,
        doc_type=doc_type,
        scroll='5m',
        timeout='5m',
        body=query,
    )

    return es_result

def handler_excel_multi_files(entName,index,res_list,cpws,sxbzxr,bgt,bzxr,ktgg,count_dict):
    if index=="judge_doc":
        x = count_dict['cpws_count']
        for res in res_list:
            tmp_dict = res['_source']
            for k,v in tmp_dict.items():
                if  k in cpws_dict:
                    num = cpws_dict[k]
                    cpws.write(x,num,str(v))
                    if "litigants" ==k:
                        name_dict = handler_special_field(entName, tmp_dict["litigants"])
                        cpws.write(x, 0, entName)
                        cpws.write(x, 1, name_dict['identity'])
                        cpws.write(x, 2, name_dict['status'])
                        cpws.write(x, 3, json.dumps(name_dict['other_name'],ensure_ascii=False))
            x+=1
        count_dict['cpws_count'] = x
    elif index=="shixin_beizhixing":
        x=count_dict['sxbzxr_count']
        for res in res_list:
            tmp_dict = res['_source']
            for k,v in tmp_dict.items():
                if  k in shixin_beizhixing_dict:
                    num = shixin_beizhixing_dict[k]
                    sxbzxr.write(x,num,str(v))
            x+=1
        count_dict['sxbzxr_count'] = x
    elif index=="exposure_desk":
        x=count_dict['bgt_count']
        for res in res_list:
            tmp_dict = res['_source']
            for k,v in tmp_dict.items():
                if  k in exposure_desk_dict:
                    num = exposure_desk_dict[k]
                    bgt.write(x,num,str(v))

            x+=1
        count_dict['bgt_count'] = x
    elif index=="executive_announcement":
        x=count_dict['bzxr_count']
        for res in res_list:
            tmp_dict = res['_source']
            for k,v in tmp_dict.items():
                if  k in executive_announcement_dict:
                    num = executive_announcement_dict[k]
                    bzxr.write(x,num,str(v))
            x+=1
        count_dict['bzxr_count'] = x
    elif index=="court_session_announcement":
        x = count_dict['ktgg_count']
        for res in res_list:
            tmp_dict = res['_source']
            ktgg.write(x, 0, entName)
            for k, v in tmp_dict.items():
                if k in court_session_announcement_dict:
                    num = court_session_announcement_dict[k]
                    ktgg.write(x, num, str(v))
            x += 1
        count_dict['ktgg_count'] = x
def handler_excel_single_file(entName,index,res_list,book):

    if index=="judge_doc":
        cpws = book.add_sheet("裁判文书")
        cpws.write(0, 0, "企业名称")
        cpws.write(0, 1, "身份")
        cpws.write(0, 2, "状态")
        cpws.write(0, 3, "其他当事人")
        cpws.write(0, 4, "当事人")
        cpws.write(0, 5, "案件名称")
        cpws.write(0, 6, "案由")
        cpws.write(0, 7, "审理法院")
        cpws.write(0, 8, "审判程序")
        cpws.write(0, 9, "来源")
        cpws.write(0, 10, "代理人")
        cpws.write(0, 11, "法院层级")
        cpws.write(0, 12, "裁判日期")
        cpws.write(0, 13, "判决结果")
        cpws.write(0, 14,"裁判文书内容")
        cpws.write(0, 15, "文书类型")
        cpws.write(0, 16, "案件类型")
        cpws.write(0, 17, "案号")
        cpws.write(0, 18, "法院人员")
        x=1
        for res in res_list:
            tmp_dict = res['_source']
            for k,v in tmp_dict.items():
                if  k in cpws_dict:
                    num = cpws_dict[k]
                    cpws.write(x,num,str(v))
                    if "litigants" ==k:
                        name_dict = handler_special_field(entName, tmp_dict["litigants"])
                        cpws.write(x, 0, entName)
                        cpws.write(x, 1, name_dict['identity'])
                        cpws.write(x, 2, name_dict['status'])
                        cpws.write(x, 3, json.dumps(name_dict['other_name'],ensure_ascii=False))
            x+=1

    elif index=="shixin_beizhixing":

        sxbzxr = book.add_sheet("失信被执行人")
        sxbzxr.write(0, 0, "被执行人姓名/名称")
        sxbzxr.write(0, 1, "案号")
        sxbzxr.write(0, 2, "被执行人年龄")
        sxbzxr.write(0, 3, "被执行人性别")
        sxbzxr.write(0, 4, "证件号码/组织机构代码")
        sxbzxr.write(0, 5, "法定代表人姓名")
        sxbzxr.write(0, 6, "执行法院")
        sxbzxr.write(0, 7, "省份")
        sxbzxr.write(0, 8, "被执行人类型")
        sxbzxr.write(0, 9, "执行依据文书编号")
        sxbzxr.write(0, 10, "立案日期")
        sxbzxr.write(0, 11, "经办机构（做出执行依据单位）")
        sxbzxr.write(0, 12, "生效法律文书确定的义务")
        sxbzxr.write(0, 13, "履行情况")
        sxbzxr.write(0, 14, "已履行部分"),
        sxbzxr.write(0, 15, "未履行部分")
        sxbzxr.write(0, 16, "失信被执行人行为具体情形")
        sxbzxr.write(0, 17, "发布时间")
        sxbzxr.write(0, 18, "来源")
        x=1
        for res in res_list:
            tmp_dict = res['_source']
            for k,v in tmp_dict.items():
                if  k in shixin_beizhixing_dict:
                    num = shixin_beizhixing_dict[k]
                    sxbzxr.write(x,num,str(v))
            x+=1
    elif index=="exposure_desk":

        bgt = book.add_sheet("曝光台")
        bgt.write(0, 0, "发布/曝光日期")
        bgt.write(0, 1, "申请执行人")
        bgt.write(0, 2, "执行金额")
        bgt.write(0, 3, "曝光类型")
        bgt.write(0, 4, "来源")
        bgt.write(0, 5, "地址")
        bgt.write(0, 6, "被执行人姓名/名称")
        bgt.write(0, 7, "执行法院")
        bgt.write(0, 8, "限制原因")
        bgt.write(0, 9, "案号")
        bgt.write(0, 10, "法院电话")
        x=1
        for res in res_list:
            tmp_dict = res['_source']
            for k,v in tmp_dict.items():
                if  k in exposure_desk_dict:
                    num = exposure_desk_dict[k]
                    bgt.write(x,num,str(v))
            x+=1
    elif index=="executive_announcement":

        bzxr = book.add_sheet("被执行人")
        bzxr.write(0, 0, "被执行人姓名/名称")
        bzxr.write(0, 1, "案号")
        bzxr.write(0, 2, "地址")
        bzxr.write(0, 3, "被执行人性别")
        bzxr.write(0, 4, "ID")
        bzxr.write(0, 5, "被执行人年龄")
        bzxr.write(0, 6, "执行金额")
        bzxr.write(0, 7, "未执行金额")
        bzxr.write(0, 8, "被执行人类型")
        bzxr.write(0, 9, "执行法院")
        bzxr.write(0, 10, "来源")
        bzxr.write(0, 11, "案件ID")
        bzxr.write(0, 12, "立案日期")
        bzxr.write(0, 13, "证件号码/组织机构代码")
        bzxr.write(0, 14, "法定代表人姓名")
        x=1
        for res in res_list:
            tmp_dict = res['_source']
            for k,v in tmp_dict.items():
                if  k in executive_announcement_dict:
                    num = executive_announcement_dict[k]
                    bzxr.write(x,num,str(v))
            x+=1

    elif index=="court_session_announcement":

        ktgg = book.add_sheet("开庭公告")
        ktgg.write(0, 0, "案由")
        ktgg.write(0, 1, "案号")
        ktgg.write(0, 2, "开庭时间")
        ktgg.write(0, 3, "法庭")
        ktgg.write(0, 4, "应诉方名字")
        ktgg.write(0, 5, "来源")
        ktgg.write(0, 6, "承办部门")
        ktgg.write(0, 7, "正文")
        ktgg.write(0, 8, "案由编码一级")
        ktgg.write(0, 9, "案由编码二级")
        ktgg.write(0, 10, "案由编码三级")
        ktgg.write(0, 11, "案由编码四级")
        ktgg.write(0, 12, "案由编码五级")
        ktgg.write(0, 13, "当事人姓名")
        ktgg.write(0, 14, "法官")
        ktgg.write(0, 15, "法院")
        ktgg.write(0, 16, "开庭日期")
        ktgg.write(0, 17, "起诉方名字")
        x = 1
        for res in res_list:
            tmp_dict = res['_source']
            for k, v in tmp_dict.items():
                if k in court_session_announcement_dict:
                    num = court_session_announcement_dict[k]
                    ktgg.write(x, num, str(v))
            x += 1
# 将文件夹zip压缩
def make_zip(input_dir, output_filename):

  f = zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED)
  for dirpath, dirnames, filenames in os.walk(input_dir):
      for filename in filenames:
          f.write(os.path.join(dirpath, filename))
  f.close()

def handler_special_field(entName,tmp_list):
    tmp_dict = {}
    tmp_dict['identity'] =""
    tmp_dict['status'] =""
    tmp_dict['other_name']=[]
    for item in tmp_list:
        if item['name']==entName:
            tmp_dict['identity']= item['identity']
            tmp_dict['status'] = item['status']
        elif item['name']!=entName:
            tmp_dict['other_name'].append(item['name'])

    return tmp_dict