from multiprocessing import Process, Pool
import itertools
import shutil
import subprocess
import re
import os
from pathlib import Path
import math
import copy
import time
import numpy as np

stop_flag = ['w', 'c', 'u','d', 'p', 't', 'uj', 'm', 'f', 'r']
# stop_flag = ['w']

def getData(path):
    data_w_dic = {}
    data_p_dic = {}
    with open(path, "r", encoding = "gbk") as f:
        lines = f.readlines()
        for line in lines:
            if line == "\n":
                continue
            arr = line.split("  ")[:-1]
            key = arr[0][0:arr[0].find("/m") - 4]
            arr = arr[1:]
            for a in arr:
                w = a[:a.find("/")]
                p = a[a.find("/") + 1:]
                if p in stop_flag:
                    continue
                if key not in data_w_dic:
                    data_w_dic[key] = []
                    data_p_dic[key] = []
                data_w_dic[key].append(w)
                data_p_dic[key].append(p)
    return data_w_dic, data_p_dic

def getAllDic(data_dic):
    all_dic = {}
    for k, v in data_dic.items():
        one_dic = getOneDic(v)
        if k not in all_dic:
            all_dic[k] = one_dic
    return all_dic

def getOneDic(one_data):
    one_dic = {}
    for a in one_data:
        if a not in one_dic:
            one_dic[a] = 0
        one_dic[a] += 1
    return one_dic

def tf(word, data_one):
    return data_one[word] / sum(data_one.values())

def df(word, data_all):
    cnt = 0
    for data in data_all:
        if word in data:
            cnt += 1
    return cnt

def idf(word, data_all):
    return math.log((len(data_all) / (df(word, data_all) + 1)), 10)

def getTfIdf(word, data_one, data_all):
    return tf(word, data_one) * idf(word, data_all)

def getOneHotList(data_all):
    keywords_list = []
    for k, v in data_all.items():
        scores = {}
        for word in v:
            scores[word] = getTfIdf(word, v, data_all)
        scores_sorted = sorted(scores.items(), key = lambda s : s[1], reverse=True)
        for i in range(10):
            if i < len(scores_sorted):
                keywords_list.append(scores_sorted[i][0])
    keywords_list = list(set(keywords_list))
    onehot_list = np.zeros((len(data_all), len(keywords_list)), dtype = np.int64)
    i = 0
    for k, v in data_all.items():
        for word in v:
            if word in keywords_list:
                onehot_list[i][keywords_list.index(word)] = 1
        i += 1
    return onehot_list

def getSimilarity(a, b):
    up = np.dot(a, b)
    down = (np.sum(a * a) ** 0.5) * (np.sum(b * b) ** 0.5)
    return up / down 

def getRowSimilarity(onehot_i, onehot_list):
	similirity_one = [0 for j in range(len(onehot_list))]
	for j, onehot_j in enumerate(onehot_list):
		similirity_one[j] = getSimilarity(onehot_i, onehot_j)
	return similirity_one


if __name__ == '__main__':
    data = getData("199801_clear.txt")
    data_w = data[0]
    data_p = data[1]
    all_dic = getAllDic(data_w)
    pool = Pool(4)
    print("预处理结束")
    start1 = time.time()
    onehot_list = getOneHotList(all_dic)
    end1 = time.time()
    print("构建向量用时：", end1 - start1)
    start2 = time.time()
    similirities = []
    for i, onehot_i in enumerate(onehot_list):
    	similirity_one = pool.apply_async(getRowSimilarity, args=(onehot_i, onehot_list))
    	similirities.append(similirity_one.get())
    end2 = time.time()
    print("计算相似度用时：", end2 - start2)
