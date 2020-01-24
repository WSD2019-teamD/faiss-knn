import os
import time
import datetime
import pandas as pd
import requests

url = 'https://qiita.com/api/v2/items'

h = {'Authorization': 'Bearer <access-token>'}

sleep_sec = 3.6

def get_simple_df(df):
    df['tags_str'] = df['tags'].apply(
        lambda tags: ','.join(tag['name'] for tag in tags if not tag['name'] == '\x00')
    )
    df['title'] = df['title'].str.replace('\r', '')
    return df[['title', 'id', 'created_at', 'updated_at','likes_count', 'comments_count', 'tags_str',
               'user_id', 'user_permanent_id', 'url']]

# Qiitaから (start, end) の範囲で記事を取得
def get_items(start, end):
    p = {
        'per_page': 100,
        'query': 'created:>{} created:<{}'.format(start, end)
    }

    time.sleep(sleep_sec)
    r = requests.get(url, params=p, headers=h)
    total_count = int(r.headers['Total-Count'])

    if total_count == 0:
        return

    df_list = [get_simple_df(pd.io.json.json_normalize(r.json(), sep='_'))]    

    if total_count > 100:
        for i in range(2, (total_count - 1) // 100 + 2):
            p['page'] = i
            time.sleep(sleep_sec)
            r = requests.get(url, params=p, headers=h)
            df_list.append(get_simple_df(pd.io.json.json_normalize(r.json(), sep='_')))

    df_all = pd.concat(df_list, ignore_index=True)

    return df_all

end = datetime.date.today()
start = end - datetime.timedelta(days=2)
new_df = get_items(start, end)
