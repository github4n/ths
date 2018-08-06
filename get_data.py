#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import pandas as pd
from get_json import get_token
from math import floor, ceil
import time

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

def get_data(query):

    token, total_row = get_token.get_token(query)
    pages = ceil(int(total_row)/70)
    print(token)
    print(pages)
    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"token\"\r\n\r\n"+ token +\
              "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"p\"\r\n\r\n1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"perpage\"\r\n\r\n70\r\n------" \
                      "WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"showType\"\r\n\r\n[\"\",\"\",\"onTable\",\"onTable\",\"onTable\"]\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
    response = requests.request("POST", url, data=payload.encode(encoding='UTF-8'), headers=headers,timeout =5)
    result = response.json()
    # print(type(result['title']))
    result_new = []   # 表头
    for i in result['title']:
        j = i.replace('\r', '')
        result_new.append(j.replace('<br>', ''))

    df1 = pd.DataFrame.from_dict(result_new).T   # 表头
    df1.to_csv("E:/iwen/data/iwen.csv",mode='a',header=False,index=False,encoding='GBK')
    df2 = pd.DataFrame.from_dict(result['result'])  # 表体
    df2.to_csv("E:/iwen/data/iwen.csv", mode='a',header=False,index=False,encoding='GBK')

    if pages >= 2:
        for p in range(2, pages + 1):
            payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"token\"\r\n\r\n" + token + \
                      "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"p\"\r\n\r\n" \
                      + str(p) + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"perpage\"\r\n\r\n70\r\n------" \
                     "WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"showType\"\r\n\r\n[\"\",\"\",\"onTable\",\"onTable\",\"onTable\"]\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
            time.sleep(3)
            response = requests.request("POST", url, data=payload.encode(encoding='UTF-8'), headers=headers,timeout =10)
            result = response.json()

            df2 = pd.DataFrame.from_dict(result['result'])  # 表体
            df2.to_csv("E:/iwen/data/iwen.csv", mode='a',header=False,index=False, encoding='GBK')
    print('导出成功！')


# get_data("预测涨停板")
# get_data("业绩预增")
get_data("大单净量>0.5")
