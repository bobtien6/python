import time
import requests
import json
from datetime import datetime

url = 'https://api.fugle.tw/realtime/v0.3/intraday/chart?symbolId=2884&apiToken=demo'
def change_time(unix_ts):
    asia_time = datetime.utcfromtimestamp(unix_ts/1000+28800)
    return asia_time

while True:
    res = requests.get(url).content
    data = json.loads(res)
    realtime = list(data['data']['chart']['t'])[-1]

    chart_data = data['data']['chart']
    print(change_time(realtime), {'average': chart_data['a'][-1], 'open': chart_data['o'][-1], 'high': chart_data['h'][-1], 'low': chart_data['l'][-1], 'close': chart_data['c'][-1], 'volumn': chart_data['v'][-1]})
    time.sleep(3)