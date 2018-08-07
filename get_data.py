#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append("..")
import requests
import pandas as pd
from get_json import get_token
from math import ceil
import time
import datetime
now = datetime.datetime.now().strftime('%Y%m%d%H%M')

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

    base_path = "E:/iwen/data/" + now   # 文件名
    save_path = base_path + ".csv"
    xlsx_path = base_path + ".xlsx"

    token, total_row = get_token.get_token(query) # 获取本次查询token值
    pages = ceil(int(total_row)/70)
    # print('token=', token)
    # print('页数：',pages)

    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"token\"\r\n\r\n"+ token +\
              "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"p\"\r\n\r\n1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"perpage\"\r\n\r\n70\r\n------" \
                      "WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"showType\"\r\n\r\n[\"\",\"\",\"onTable\",\"onTable\",\"onTable\"]\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
    response = requests.request("POST", url, data=payload.encode(encoding='UTF-8'), headers=headers,timeout =5)
    result = response.json()  # 返回首页结果
    # print(type(result['title']))
    result_new = []   # 表头
    for i in result['title']:
        j = i.replace('\r', '')
        result_new.append(j.replace('<br>', ''))

    df1 = pd.DataFrame.from_dict(result_new).T   # 表头
    df1.to_csv(save_path,mode='a',header=False,index=False,encoding='GBK')
    df2 = pd.DataFrame.from_dict(result['result'])  # 首页表体
    df2.to_csv(save_path, mode='a',header=False,index=False,encoding='GBK')

    if pages >= 2:
        for p in range(2, pages + 1):
            payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"token\"\r\n\r\n" + token + \
                      "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"p\"\r\n\r\n" \
                      + str(p) + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"perpage\"\r\n\r\n70\r\n------" \
                     "WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"showType\"\r\n\r\n[\"\",\"\",\"onTable\",\"onTable\",\"onTable\"]\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
            time.sleep(3)
            response = requests.request("POST", url, data=payload.encode(encoding='UTF-8'), headers=headers,timeout =10)
            result = response.json() # 返回其他页结果

            df2 = pd.DataFrame.from_dict(result['result'])  # 其他页表体
            df2.to_csv(save_path, mode='a',header=False,index=False, encoding='GBK')

    writer = pd.ExcelWriter(xlsx_path)
    condition = ['筛选条件：',query]
    condf = pd.DataFrame(condition).T
    condf.to_excel(writer, '筛选条件',header=False, index=False)  # CSV文件转XLSX  sheet1  筛选条件

    csv_to_xlsx = pd.read_csv(save_path, encoding='GBK')
    csv_to_xlsx.to_excel(writer, sheet_name='data', index=False, freeze_panes=(1, 1))  # sheet2 data
    writer.save()
    print('数据导出成功！\n保存路径：', xlsx_path)
    if os.path.exists(save_path):
        os.remove(save_path)  # 删除源CSV文件

# while True:
#     get_data(str(input('请输入筛选条件：')))
#     input('继续请按Enter键')


# get_data("预测涨停板")
# get_data("业绩预增")
get_data("大单净量>1")