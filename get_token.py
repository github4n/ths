#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests


def get_token(query):

    url = "https://www.iwencai.com/data-robot/get-fusion-data"
    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"tid\"\r\n\r\nstockpick\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW" \
              "\r\nContent-Disposition: form-data; name=\"querytype\"\r\n\r\nstock\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: " \
              "form-data; name=\"w\"\r\n\r\n"+ query +"\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"robot\"\r\n\r\n{\"source\":\"Ths_iwencai_Xuangu\",\"user_id\":\"\",\"log_info\":\"{\\\"other_info\\\":\\\"{\\\\\\\"eventId\\\\\\\":\\\\\\\"iwencai_pc_hp_history\\\\\\\",\\\\\\\"ct\\\\\\\":1533288325154}\\\",\\\"other_utype\\\":\\\"random\\\",\\\"other_uid\\\":\\\"Ths_iwencai_Xuangu_71apin2h647coi44q5cjkbhnfzaopwu9\\\"}\",\"user_name\":\"vj1zuoimhp\",\"version\":\"1.5\"}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
    headers = {
        'origin': "https://www.iwencai.com",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9",
        'hexin-v': "Ap4KH54CSa0-2p3JYsl9Btdh7z_jX2LY9CMWvUgnCuHcazTjsO-y6cSzZsQb",
        'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5702.400 QQBrowser/10.2.1893.400",
        'accept': "application/json, text/javascript, */*; q=0.01",
        'x-requested-with': "XMLHttpRequest",
        'connection': "keep-alive",
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'cache-control': "no-cache",
        'postman-token': "c773ff13-a965-5776-e3a5-d8d58d05d5b2"
        }

    response = requests.request("POST", url, data=payload.encode(encoding='UTF-8'), headers=headers,timeout =5)

    result = response.json()
    # print(result)
    token = result["data"]["wencai_data"]["result"]["token"]
    total_row = result["data"]["robot_data"]["answer"][0]["table"][0]["total_row"]
    print('token值', token)
    print('符合个数：',total_row)
    return token, total_row

# token,total_row = get_token("预测涨停板")
# print(token,total_row)