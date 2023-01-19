import requests
from bs4 import BeautifulSoup
payload = {
    'queryType': 1,
    'goDay': '',
    'doQuery': 1,
    'dateaddcnt': '',
    'queryDate': '2023/01/17',
}

oi = requests.post('https://www.taifex.com.tw/cht/3/totalTableDate', data=payload).content
# print(oi)

soup = BeautifulSoup(oi, 'html.parser').find_all('table')[4]

# print(soup)
title_list = []
for title in soup.find_all('tr'):
    title_list.append([vaule.text for vaule in title.find_all('th')])
# print(title_list)

body_list = []
for body in soup.find_all('tr'):
    body_list.append([vaule.text.replace('\n','').replace('\r','').replace('\t','').replace(' ','') for vaule in body.find_all('td')])
real_date = body_list[3:]
# print(real_date)

colname = title_list[2][1:]  # data colname
# print(colname)