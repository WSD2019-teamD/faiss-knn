import os
import datetime
import json
import pandas as pd
from urllib.parse import urlparse
from sqlalchemy import create_engine
from sqlalchemy.sql import text

with open('private.json') as f:
    dbinfo = json.load(f)['database']

db_url = dbinfo['url']
db = dbinfo['db']
table = dbinfo['table']

url = urlparse(db_url)

engine = create_engine('mysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4'.format(host = url.hostname, port=url.port, user = url.username, password= url.password, database = db),encoding='utf-8')

columns = ['article_id', 'title', 'created_at', 'updated_at', 'likes_count', 'comments_count', 'tags_str', 'user_id', 'user_permanent_id', 'url', 'html', 'tokens']
update_columns = ['title', 'updated_at', 'likes_count', 'comments_count', 'tags_str', 'user_id', 'html', 'tokens']

def insert_article_data(df, engine):
    '''
    query = text("""insert into {}.{}(article_id,
                                      title,
                                      created_at,
                                      updated_at,
                                      likes_count,
                                      comments_count,
                                      tags_str,
                                      user_id,
                                      user_permanent_id,
                                      url,
                                      html,
                                      tokens)
                values (:article_id,
                        :title,
                        :created_at,
                        :updated_at,
                        :likes_count,
                        :comments_count,
                        :tags_str,
                        :user_id,
                        :user_permanent_id,
                        :url,
                        :html,
                        :tokens)
                on duplicate key update title = :title,
                                        updated_at = :updated_at,
                                        likes_count = :likes_count,
                                        comments_count = :comments_count,
                                        tags_str = :tags_str,
                                        user_id = :user_id,
                                        html = :html,
                                        tokens = :tokens""".format(db, table))
    '''
    print('Inserting into database...')
    query = text('insert into {}.{}('.format(db, table)
            + str(columns).strip('[]').replace("'", "")
            + ') values ('
            + str([':' + s for s in columns]).strip('[]').replace("'", "")
            + ') on duplicate key update '
            + str([s + ' = :' + s for s in update_columns]).strip('[]').replace("'", ""))

    err_cnt = 0

    for _, row in df.iterrows():
        param = {}
        for c in columns:
            param[c] = row[c]
        try:
            engine.execute(query, **param)
        except Exception as e:
            print('type:' + str(type(e)))
            print('args:' + str(e.args))
            print('error:' + str(e))
            err_cnt += 1
            pass
    
    if err_cnt == 0:
        print('Insertion successfully completed.')
    else:
        print('{} errors occured.'.format(err_cnt))

if __name__ == "__main__":
    from get_content import get_items
    end = datetime.date.today()
    start = end - datetime.timedelta(days=2)
    df = get_items(start, end)

    insert_article_data(df, engine)