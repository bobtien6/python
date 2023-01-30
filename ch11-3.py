import json
import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    'content-type': 'text/html; charset=UTF-8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}

def earning_ratio_ex(date, rank=None): #上市
    url = 'https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=json&date={}&selectType=ALL&_=1605843766573'.format(date)
    data = json.loads(requests.get(url, headers=headers).content)
    df = pd.DataFrame(data['data'], columns=data['fields'])
    df = df.sort_values(by=['殖利率(%)'], ascending=False).iloc[:rank]
    df.to_csv('earning_ratio_exchange_{}.csv'.format(date), index=False)

def earning_ratio_co(date, rank=None): #上櫃
    url = 'https://www.tpex.org.tw/web/stock/aftertrading/peratio_analysis/pera_result.php?l=zh-tw&d={}&c=&_=1605844331685'.format(date)  #日期要填民國的，例如109/11/19
    data = json.loads(requests.get(url).content)
    title = ['股票代號', '名稱', '本益比', '每股股利', '股利年度', '殖利率(%)', '股價淨值比']
    df = pd.DataFrame(data['aaData'], columns=title)
    df = df.sort_values(by=['殖利率(%)'], ascending=False).iloc[:rank]
    df.to_csv('earning_ratio_counter_{}.csv'.format(date.replace('/', '')), index=False)


earning_ratio_ex('20221118', 10)
earning_ratio_co('111/11/18', 10)
