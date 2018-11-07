#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8

import re
import requests
import  pandas as pd
from bs4 import BeautifulSoup

def Get_Data(content):

    list = []
    for x in range(1,286):
        url = 'http://srh.bankofchina.com/search/whpj/search.jsp?erectDate=2018-09-1&nothing=2018-10-23&pjname=%d&page=%d'%(content,x)
        html = requests.get(url).content.decode('utf-8')
        s = html
        result = re.findall('<td>(.*?)</td>',s)

        listmin = []
        for x in result:
            if (result.index(x)) % 7== 1 and result.index(x) >0 :
                if listmin[0] =='&nbsp;':
                    pass
                else:
                    list.append(listmin)
                listmin = []
            listmin.append(x)
    return pd.DataFrame(list[1:],columns=['货币名称','现汇买入价','现钞买入价','现汇卖出价','现钞卖出价','中行折算价','发布时间'])

if __name__ == '__main__':

    # Coin = [1315,1323,1316,1326]
    # National =['HK','Japan','US','EU']
    Coin = [1316]
    National =['US']

    for x in Coin:
        df = Get_Data(x)
        file_path = r'./%s.xlsx'%National[Coin.index(x)]
        writer = pd.ExcelWriter(file_path)
        df.to_excel(writer, index=False, encoding='utf-8', sheet_name='Sheet')
        writer.save()

    # content = 1314
    # response = requests.get(
    #     'http://srh.bankofchina.com/search/whpj/search.jsp?erectDate=2018-09-1&nothing=2018-10-23&pjname=%d&page=1' % content)
    # soup = BeautifulSoup(response.text, 'lxml')
    # print(soup)
    # gbt_state_line = soup.find()
    #
    # print(gbt_state_line)