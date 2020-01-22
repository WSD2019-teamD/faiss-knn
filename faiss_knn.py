import numpy as np
import pandas as pd
import time
import glob
import faiss
import sys
import os

path = r'data/vec.csv'

print('Loading csv...')
df_vec = pd.read_csv('./data/vec.csv')

df_vec = df_vec[df_vec['vec50'] != '[]'] #vec50が空のものを落とす
df_vec = df_vec.reset_index()            #indexを修正
df_vec = df_vec.drop('index',axis=1)

dic = {}
for i, id in enumerate(df_vec['id']):
    dic[id] = i


def parseVector(string):
    lst = string.strip('[]').replace('(', '').replace(')', '').replace(' ', '').split(',')
    v = [float(lst[2*i + 1]) for i in range(len(lst) // 2)]
    return v

print('Creating NumPy array...')

arr = [parseVector(s) for s in df_vec['vec50']]

dim = len(arr[0])   # ベクトルの次元(dimension)
nb = len(arr)       # データベースのサイズ(database size)
nq = 1              # クエリベクトルの数(nb of queries)

xb = np.array(arr).astype('float32')

print('Building index...')
index = faiss.IndexFlatL2(dim)
index.add(xb)


def search_knn(target_id, count):
    s = time.time()
    qid = dic[target_id]
    xq = np.array(arr[qid:qid+1]).astype('float32')
    D, I = index.search(xq, count)

    res = {}
    for i, d in zip(I[0], D[0]):
        id = df_vec['id'][i]
        res[id] = float(d)
    
    e = time.time()
    print("search time: {}".format(e-s))
    
    return res
