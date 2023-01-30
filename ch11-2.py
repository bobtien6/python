import json
import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    'content-type': 'text/html; charset=UTF-8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}

def dividen_ex(start, end): #上市

    url = 'https://www.twse.com.tw/exchangeReport/TWTAWU?response=json&startDate={}&endDate={}&stockNo=&querytype=3&selectType=&_=1605842353705'.format(start, end)
    data = json.loads(requests.get(url, headers=headers).content)    # print(data)
    df = pd.DataFrame(data['data'], columns=data['fields'])
    df.to_csv('{}-{}_dividen_exchange.csv'.format(start,end), index=False)

def dividen_co(start): #上櫃
    url = 'https://www.tpex.org.tw/web/stock/aftertrading/cmode/chtm_result.php?l=zh-tw&o=json&d={}'.format(start) #日期要填民國的，例如109/11/19
    data = json.loads(requests.get(url, headers=headers).content)

    for index, row in enumerate(data['aaData']):
        data['aaData'][index] = row[:7]
        #如果要處理空格或是Y的話再另外處理

    title = ['證券代號', '證券名稱', '變更交易', '分盤交易', '屬管理股票', '分盤或管理股票撮合循環時間(分鐘)', '停止交易']
    df = pd.DataFrame(data['aaData'], columns=title)
    df.to_csv('{}_dividen_counter.csv'.format(start.replace('/', '')), index=False)


dividen_ex(20201001,20201118)
dividen_co('109/11/19')