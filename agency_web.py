import requests
import pandas as pd
import time
import datetime


from config import agency_web_url
dfs = []

for page in range(0,3158):

    payload = f"lyzarea_id=&lyztown_id=&subway_id=&subway_items_id=&page={page}&keyword="
    headers = {
      'authority': 'www.jiazaishanghai.com',
      'accept': 'application/json, text/javascript, */*; q=0.01',
      'accept-language': 'zh-CN,zh;q=0.9',
      'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
      'cookie': 'kefu_user=56103%7C864000%7C1681441610%7C5de322cf43a8b0bc571128386cf54789; Hm_lvt_44358024198b1fa6b5dba03fa558aa3e=1679320714,1679473914,1680577608,1680681330; PHPSESSID=5msv4t6sgo0efbmnmh6d2eod51; Hm_lpvt_44358024198b1fa6b5dba03fa558aa3e=1680688064',
      'origin': 'https://www.jiazaishanghai.com',
      'referer': 'https://www.jiazaishanghai.com/index/houses/houses/index.html?keyword=',
      'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-origin',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
      'x-requested-with': 'XMLHttpRequest'
    }

    response = requests.request("POST", agency_web_url, headers=headers, data=payload)

    df = pd.DataFrame.from_dict(response.json()['data']['rows'])

    dfs.append(df)


result_df = pd.concat(dfs, ignore_index=True)
