# -*- coding:utf-8 -*-
import urllib2

lists = CellRange('a2:a2500').value
s_list = ''
for i in lists:
    if i != None:
        t = i.split('.')
        new = t[1].lower() + t[0]
        s_list = s_list + new + ','
# print(s_list)
url = "https://hq.sinajs.cn/list="+ s_list

response = urllib2.urlopen(url)
# print(response.read())
text = response.read()
t_list = text.split(',')
# print(t_list)
price = []
zhangfu = []
for i in t_list:
    if 'var hq_str_' in i:
        index = t_list.index(i)
        # print(index)
        # print(t_list[index + 1], t_list[index + 2], t_list[index + 3])

        price.append(t_list[index + 3])


        zf = (float(t_list[index + 3]) - float(t_list[index + 2])) / float(t_list[index + 2]) * 100
        zf = ("%.3f" % zf)
        zhangfu.append(zf)

# print('现价：', price)
# print('涨幅：', zhangfu)

# for i in price:
#    index = price.index(i)
#    print(index)
#    Cell(index+1,"C").value = i
insert_col(3)
insert_col(3)
Cell("C1").horizontal = [u'现价(元)',u'涨跌幅(%)']
CellRange("C1:D1").color = 15649709
Cell("C2").vertical = price
Cell("D2").vertical = zhangfu



