import requests
import json
from datetime import datetime

url = 'https://api.fugle.tw/realtime/v0.3/intraday/chart?symbolId=2884&apiToken=demo'
res = requests.get(url).content
data = json.loads(res)
print(data['data']['chart'])

realtime = list(data['data']['chart']['t'])
print(realtime) #unix timestamp with millisecond
# utc_time = datetime.utcfromtimestamp(realtime/1000)
# asia_time = datetime.utcfromtimestamp(realtime/1000+28800)
# print(utc_time)
# print(asia_time)

def change_time(unix_ts):
    # utc_time = datetime.utcfromtimestamp(unix_ts / 1000)
    asia_time = datetime.utcfromtimestamp(unix_ts/1000+28800)
    return asia_time

for i in realtime:
    print(change_time(i))
