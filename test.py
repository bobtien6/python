import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

data = ''
while data == '':
    try:
        # res = requests.get('https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=html&date=20221201&stockNo=2330', verify=False)
        f = open('/Users/mac/work/python/2330_20221201.html', 'r')  #local file
        s = f.read()
        break
    except:
        time.sleep(1)
        print('zzz...')

soup_title = BeautifulSoup(s, 'html.parser').find('thead').find('tr').text
title = soup_title.replace('\n', '').split(' ')[1:3]

soup_body = BeautifulSoup(s, 'html.parser').find_all('tr')
datalist = []

for col in soup_body:
    datalist.append([row.text for row in col.find_all('td')])

def transfer_date(date):
    y, m, d = date.split('/')
    return '{}/{}/{}'.format(str(int(y)+1911), m, d)

for index, i in enumerate(datalist):
    if index > 1:
        datalist[index][0] = transfer_date(i[0])

datalist = datalist[1:]
df = pd.DataFrame(datalist)
# print(df)
# df.to_csv('{}{}.csv'.format(title[0],title[1]), index=False, header=False, mode='w')
df[1:].to_csv('{}{}.csv'.format(title[0],title[1]), index=False, header=False, mode='w')