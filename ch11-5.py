import os.path

import requests
import json
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

def transfer_date(date):  # 民國轉西元
    y, m, d = date.split('/')
    return '{}/{}/{}'.format(int(y)+1911, m, d)
# print(transfer_date('109/01/05'))

headers = {
    'content-type': 'text/html; charset=UTF-8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}

def get_data(date, stockNo):
    # url = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=html&date={}&stockNo={}".format(date, stockNo)
    # data = requests.get(url, headers=headers).content
    f = open('/Users/mac/work/python/ch11-4_web.html', 'r')  # local file
    data = f.read()
    title = BeautifulSoup(data, 'html.parser').find('thead').find('tr')

    datalist = []
    for col in title.find_all_next('tr'):
        datalist.append([row.text for row in col.find_all('td')])

    for item in datalist[1:]:
        item[0] = transfer_date(item[0])

    df = pd.DataFrame(datalist[1:], columns=datalist[:1])
    df.columns = datalist[0]

    df.to_csv('{}_{}.csv'.format(date, stockNo), index=False)


def duration(start_year, start_month, end_year, end_month):
    for year in range(start_year, end_year+1):
        # 開始年份和結束年份相同
        if start_year == end_year:
            for month in range(start_month, end_month+1):
                print('{}{}01'.format(year,str(month).zfill(2)))
            break

        # 開始年份和結束年份不同
        if year == start_year:
            for month in range(start_month, 13):
                print('{}{}01'.format(year,str(month).zfill(2)))
        elif year == end_year:
            for month in range(1, end_month+1):
                print('{}{}01'.format(year,str(month).zfill(2)))
        else:
            for month in range(1, 13):
                print('{}{}01'.format(year,str(month).zfill(2)))

duration(2019, 3, 2021, 11)
