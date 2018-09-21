#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import requests
import pandas as pd
from math import ceil
import time
import datetime
sys.path.append("..")
from get_json import get_token
from sqlalchemy import create_engine
engine = create_engine('mssql+pymssql://sa:kingdee@2018@localhost:1433/db?charset=utf8') # ,echo = True  # echo 是否显示数据库执行过程


url = "https://www.iwencai.com/stockpick/cache"
headers = {
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.9",
    'hexin-v': "Ah96v4m6uLJiMbyugxHsKd7KrniqhHOWjdh3ErFsu04VQDVkuVQDdp2oB2TC",
    'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5702.400 QQBrowser/10.2.1893.400",
    'accept': "application/json, text/javascript, */*; q=0.01",
    'x-requested-with': "XMLHttpRequest",
    'connection': "keep-alive",
    'content-encoding': "gzip",
    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    'cache-control': "no-cache",
    'postman-token': "b10e6bdb-b7bf-1dc2-fdf4-5aa2552ec454"
}


def get_data(query,table_name):
    # now = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    timestamp = datetime.datetime.now().strftime('%H:%M:%S')

    token, total_row = get_token.get_token(query) # 获取本次查询token值
    pages = ceil(int(total_row)/70)
    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"token\"\r\n\r\n"+ token +\
              "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"p\"\r\n\r\n1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"perpage\"\r\n\r\n70\r\n------" \
                      "WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"showType\"\r\n\r\n[\"\",\"\",\"onTable\",\"onTable\",\"onTable\"]\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
    response = requests.request("POST", url, data=payload.encode(encoding='UTF-8'), headers=headers,timeout =5)
    result = response.json()  # 返回首页结果
    result_title,result_detail,is_merge = get_title(result['title'])

    body = get_body(result['result'])  # 首页表体
    df1 = pd.DataFrame.from_dict(body)
    df_all= df1

    # 获取其他页表体
    if pages >= 2:
        for p in range(2, pages + 1):
            payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"token\"\r\n\r\n" + token + \
                      "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"p\"\r\n\r\n" \
                      + str(p) + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"perpage\"\r\n\r\n70\r\n------" \
                     "WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"showType\"\r\n\r\n[\"\",\"\",\"onTable\",\"onTable\",\"onTable\"]\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
            time.sleep(3)
            response = requests.request("POST", url, data=payload.encode(encoding='UTF-8'), headers=headers,timeout =10)
            result = response.json() # 返回其他页结果
            other_body = get_body(result['result'])
            df_body_other = pd.DataFrame.from_dict(other_body)  # 其他页表体
            df_all = df_all.append(df_body_other,ignore_index=True)  # 拼接 3
        df_all.columns = result_title
        df1.loc[:, "date"] = date
        df1.loc[:, "time"] = timestamp
        df_all.to_sql(table_name, engine, if_exists='append',index=False)
    else:
        df1.columns = result_title
        df1.loc[:, "date"] = date
        df1.loc[:, "time"] = timestamp
        df1.to_sql(table_name, engine, if_exists='append',index=False)

    print('数据导出成功!\n')


# 获取表头
def get_title(title_result):
    result_title = []
    result_detail = []
    if '{' in str(title_result):
        is_merge = 1
        for i in title_result:
            if isinstance(i, str):
                j = i.replace('\r', '').split('<br>')[0]
                result_detail.append('')
                result_title.append(j)

            if isinstance(i, dict):
                (key, value), = i.items()
                key = key.replace('\r', '').split('<br>')[0]
                result_detail.append(key)
                for d in value[1:]:
                    result_detail.append('')
                for v in value:
                    result_title.append(v)
    else:
        is_merge = 0
        for i in title_result:
             j = i.replace('\r', '').replace('(','（').replace(')','）').split('<br>')[0]
             result_title.append(j)
    return result_title,result_detail,is_merge


# 获取表体
def get_body(body_result):
    # 处理一个单元格下存在多个表格情况, # print(result[0][4][0]['UID']) # 定位到字典里的值
    body = []
    for solo in body_result:
        new_list = []
        if isinstance(solo, list):
            for zi in solo:
                if isinstance(zi, list):
                    st = ''
                    for value in zi:
                        if isinstance(value, dict):
                            for id in value:
                                st = str(value[id]) + '。' + st
                        else:
                            new_list.append(value)
                    if st == '':
                        pass
                    else:
                        new_list.append(st)
                else:
                    new_list.append(zi)
        else:
            new_list.append(solo)
        body.append(new_list)
    return body



# 程序入口
# get_data("预测涨停板",'zhangting')
# input('enter to end')
# get_data("量比排名前20",'liangbi')
# get_data("换手率排名前10",'huanshoulv')
# get_data("大单净量>0 筹码集中")

# get_data("近2天公告利好")
# get_data("连续3日 dde大单净量大于0.3")
# get_data("业绩预增")
# get_data("连续5日 换手率>7")
