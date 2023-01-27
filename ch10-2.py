import requests
import json
from datetime import datetime

url = 'https://api.fugle.tw/realtime/v0.3/intraday/chart?symbolId=2884&apiToken=demo'
res = requests.get(url).content
data = json.loads(res)

realtime = list(data['data']['chart']['t'])
# print(realtime) #unix timestamp with millisecond

# chart_data = list(data['data']['chart'].values())
chart_data = data['data']['chart']
# print(chart_data)
def change_time(unix_ts):
    # utc_time = datetime.utcfromtimestamp(unix_ts / 1000)
    asia_time = datetime.utcfromtimestamp(unix_ts/1000+28800)
    return asia_time

tmp = []
for index, i in enumerate(realtime):
    print(change_time(i), {'average': chart_data['a'][index], 'open': chart_data['o'][index], 'high': chart_data['h'][index], 'low': chart_data['l'][index], 'close': chart_data['c'][index], 'volumn': chart_data['v'][index]})
    # tmp.append({'average': chart_data['a'][index], 'open': chart_data['o'][index], 'high': chart_data['h'][index], 'low': chart_data['l'][index], 'close': chart_data['c'][index], 'volumn': chart_data['v'][index]})


# for i, j in zip(realtime, tmp):
#     print(change_time(i), j)

