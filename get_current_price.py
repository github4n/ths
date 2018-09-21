# -*- coding:utf-8 -*-
import requests
import pandas as pd
import datetime
from sqlalchemy import create_engine
engine = create_engine('mssql+pymssql://sa:kingdee@2018@localhost:1433/db?charset=utf8') # ,echo = True  # echo 是否显示数据库执行过程

data = pd.read_sql_query("SELECT 股票代码 FROM huanshoulv where [上市天数（天）]<100",con = engine)  # 取需要查询代码
lists = data['股票代码'].values.tolist()

s_list = ''
for i in lists:
    if i != None:
        t = i.split('.')
        new = t[1].lower() + t[0]
        s_list = s_list + new + ','
# print(s_list)

url = "https://hq.sinajs.cn/list="+ s_list

response = requests.get(url)  # 从新浪网获取最新信息
text = response.text
t_list = text.split(',')
price = []
zhangfu = []
for i in t_list:
    if 'var hq_str_' in i:
        index = t_list.index(i)
        price.append(t_list[index + 3])

        zf = (float(t_list[index + 3]) - float(t_list[index + 2])) / float(t_list[index + 2]) * 100
        zf = ("%.3f" % zf)
        zhangfu.append(zf)

date = datetime.datetime.now().strftime('%Y-%m-%d')
timestamp = datetime.datetime.now().strftime('%H:%M:%S')
current = [lists,price,zhangfu]
df_cur = pd.DataFrame.from_dict(current).T
df_cur.loc[:, "date"] = date
df_cur.loc[:, "time"] = timestamp
df_cur.columns = ['股票代码','现价（元）','涨幅（%）','date','time']     # 新表字段名

# print(df_cur)
df_cur.to_sql('current_price', engine, if_exists='append',index=False)  # 重新存入另外一个表current_price




