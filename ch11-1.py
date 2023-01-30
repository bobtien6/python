import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    'content-type': 'text/html; charset=UTF-8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}

def print_list(input_type):
    stock_list = {'exchange': 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=2', 'counter': 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=4'}
    # 印出字型
    # print(requests.get(stock_list['exchange'], headers=headers).encoding)

    getdata = requests.get(stock_list[input_type], headers=headers).content
    soup = BeautifulSoup(getdata, 'html.parser', from_encoding='MS950').find('table', class_='h4')

    # print(soup)

    datalist = []
    for col in soup.find_all_next('tr'):
        datalist.append([row.text for row in col.find_all('td')])

    for deal_str in datalist[1:]: #第一行不是股票和代碼會出錯所以不處理
        if len(deal_str) == 7:
            name = deal_str[0].split('\u3000')[1]
            deal_str[0] = deal_str[0].split('\u3000')[0]
            deal_str.insert(1, name)

    title = ['有價證券代號', '有價證券名稱', '國際證券辨識號碼(ISIN Code)', '上市日', '市場別', '產業別', 'CFICode', '備註']
    df = pd.DataFrame(datalist[1:], columns=title)

    df.to_csv('{}_list.csv'.format(input_type), index=False)

print_list('exchange')
print_list('counter')