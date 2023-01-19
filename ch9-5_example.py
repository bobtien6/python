import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    'content-type': 'text/html; charset=UTF-8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}

# -------------  期交所 POST 未平倉 -------------------
def futures_traded(get_date):
    payload = {
        'queryType': 1,
        'goDay': '',
        'doQuery': 1,
        'dateaddcnt': '',
        'queryDate': get_date,
    }
    dividend = requests.post(' https://www.taifex.com.tw/cht/3/totalTableDate', payload)
    soup = BeautifulSoup(dividend.content, 'html.parser').find_all('table')

    titlelist = []
    for col in soup[2].find_all('tr'):
        titlelist.append([row.text.replace(' ','') for row in col.find_all('th')])

    datalist = []
    for col in soup[3].find_all('tr')[3:]:
        datalist.append([row.text.replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '') for row in col.find_all('td')])

    col_name = titlelist[4]
    col = {'身分別': [i[0] for i in titlelist[5:9]]}
    df = pd.DataFrame(datalist)
    new_colname = {}
    for i, j in zip(df.columns.tolist(), col_name[1:]):
        new_colname.update({i:j})
    df.rename(columns=new_colname, inplace=True)
    new = pd.concat([pd.DataFrame(col), df], axis=1)
    new.set_index('身分別')
    new.to_csv('futures_Traded{}.csv'.format(get_date.replace('/', '')), index=False)


def futures_OI(get_date):
    payload = {
        'queryType': 1,
        'goDay': '',
        'doQuery': 1,
        'dateaddcnt': '',
        'queryDate': get_date,
    }
    dividend = requests.post(' https://www.taifex.com.tw/cht/3/totalTableDate', payload)
    soup = BeautifulSoup(dividend.content, 'html.parser').find_all('table')

    titlelist = []
    for col in soup[4].find_all('tr'):
        titlelist.append([row.text.replace(' ','') for row in col.find_all('th')])

    datalist = []
    for col in soup[4].find_all('tr'):
        datalist.append([row.text.replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '') for row in col.find_all('td')])

    col_name = titlelist[2]
    col = {'身分別': [i[0] for i in titlelist[3:9]]}
    df = pd.DataFrame(datalist[3:])

    new_colname = {}
    for i, j in zip(df.columns.tolist(), col_name[1:]):
        if i == 0 or i == 1:
            j = '多方'+str(j)
        elif i == 2 or i == 3:
            j = '空方'+str(j)
        elif i == 4 or i == 5:
            j = '合計'+str(j)
        new_colname.update({i:j})
    df.rename(columns=new_colname, inplace=True)
    new = pd.concat([pd.DataFrame(col), df], axis=1)
    new.set_index('身分別')
    new.to_csv('futures_OI{}.csv'.format(get_date.replace('/', '')), index=False)

# futures_OI('2020/11/19')
# 課程簡易版:  爬OI
payload = {
    'queryType': 1,
    'goDay': '',
    'doQuery': 1,
    'dateaddcnt': '',
    'queryDate': '2020/11/16',
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
    body_list.append([vaule.text.replace('\n','').replace('\t','').replace(' ','') for vaule in body.find_all('td')])
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

new.to_csv('futures_oi_{}.csv'.format('20201116'), index=False, header=False)