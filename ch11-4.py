import json
import requests
from bs4 import BeautifulSoup
import pandas as pd

def transfer_date(date):
    y, m, d = date.split('/')
    return '{}/{}/{}'.format(str(int(y)+1911), m, d)

headers = {
    'content-type': 'text/html; charset=UTF-8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}

def get_data(date, stockNo):
    url = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=html&date={}&stockNo={}'.format(date, stockNo) #現在日期需要輸入西元，但是抓到的資料日期會是民國
    data = requests.get(url, headers=headers).content
    soup = BeautifulSoup(data, 'html.parser', from_encoding='utf-8')
    title = soup.find('thead').find('tr')

    datalist = []
    for col in title.find_all_next('tr'):
        datalist.append([row.text for row in col.find_all('td')])

    for item in datalist[1:]:
        # for i in item:
        #     print(i)
        # print(item)
        item[0] = transfer_date(item[0])

    df = pd.DataFrame(datalist[1:], columns=datalist[0])
    print(df)
get_data('20221118', '2330')