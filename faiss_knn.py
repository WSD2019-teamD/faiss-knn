import numpy as np
import pandas as pd
import time
import glob
import faiss
import sys

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

xb = np.array(arr).astype('float32')

print('Building index...')
index = faiss.IndexFlatL2(dim)
index.add(xb)


def search_knn(id_list, count):
    s = time.time()
    vq = []
    for id in id_list:
        vq.append(arr[dic[id]])

    xq = np.array(vq).astype('float32')
    D_all, I_all = index.search(xq, count)

    res = {}
    for D, I, qid in zip(D_all, I_all, id_list):
        inner_res = {}
        for d, i in zip(D, I):
            id = df_vec['id'][i]
            inner_res[id] = float(d)        
        res[qid] = inner_res

    e = time.time()
    print("search time: {}".format(e-s))
    
    return res
