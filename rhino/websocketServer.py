#! /user/bin/env python
# ——×—— coding:utf-8 ——×——

import asyncio,os,sys
import datetime
import random
import websockets,time


from collections import deque
# async def time(websocket, path):
#     while True:
#         now = datetime.datetime.utcnow().isoformat() + 'Z'
#         await websocket.send(now)
#         await asyncio.sleep(random.random() * 3)

# async def tail(websocket, path):
#     try:
#         dir = await websocket.recv()
#         print(dir)
#         filename = "/home/kz/log/{}.log".format(dir)
#         print(filename)
#         while True:
#             lines = '<br>'.join(list(deque(open(filename), 10)))
#             print(lines)
#             await websocket.send(lines)
#             if lines:
#                 time.sleep(1)
#                 continue
#     except Exception as e:
#         print('打开文件失败，囧，看看文件是不是不存在，或者权限有问题')
#         print(e)
async def tail(websocket, path):
    try:
        dir = await websocket.recv()
        filename = "/etc/rhino/task/{}/streaming.log".format(dir)
        print(filename)
        # 打开文件
        p = 0
        while True:
            with open(filename) as f:
                f.seek(p, 0)  # 偏移到上次结束位置
                line = f.readline()
                if line:
                    await websocket.send(line)
                # 获取当前位置，作为偏移值
                p = f.tell()
                time.sleep(0.05)
    except Exception as e:
        print('打开文件失败，囧，看看文件是不是不存在，或者权限有问题')
        print(e)



start_server = websockets.serve(tail, '127.0.0.1', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

