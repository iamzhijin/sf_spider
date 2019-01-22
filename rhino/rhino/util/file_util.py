#coding=utf-8

# Author: Ron Lin
# Date: 2017/10/31
# Email: hdsmtiger@gmail.com


from django.http import StreamingHttpResponse
import os


def big_file_download(filename):

    if not os.path.exists(filename):
        return None

    # 抽取真正的文件名
    begin = filename.rfind("/") + 1
    extract_file_name = "temp.txt"
    if begin > 0:
        extract_file_name = filename[begin: len(filename)]

    def file_iterator(file_name, chunk_size=512):
        with open(file_name, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    response = StreamingHttpResponse(file_iterator(filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(extract_file_name)

    return response
