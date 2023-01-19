import requests
from bs4 import BeautifulSoup
import pandas as pd

payload = {
    'queryType': 1,
    'goDay': '',
    'doQuery': 1,
    'dateaddcnt': '',
    'queryDate': '2023/01/17',
}

oi = requests.post('https://www.taifex.com.tw/cht/3/totalTableDate', data=payload).content
soup = BeautifulSoup(oi, 'html.parser').find_all('table')[4]
print(soup)

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

dfcol = pd.DataFrame([colname]) # colname for data check
# print(dfcol)

dfdata = pd.DataFrame(real_date)
# print(dfdata)

df = pd.concat([dfcol, dfdata], axis=0)
df = df.reset_index(drop=True)
# print(df)

col = [title_list[2][0]]
for i in title_list[3:7]:
    col = col + i

dffcol = pd.DataFrame(col)
# print(dffcol)

new = pd.concat([dffcol, df], axis=1)
# print(new)

new.to_csv('futures_oi_{}.csv'.format('20230117'), index=False, header=False)