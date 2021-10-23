import shutil
import subprocess
import re
import os
from pathlib import Path
import math
import copy
import time

stop_flag = ['w', 'c', 'u','d', 'p', 't', 'uj', 'm', 'f', 'r']
# stop_flag = ['w']
s = 0.2

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

def getLenDic(all_dic):
    len_dic = {}
    for k, v in all_dic.items():
        if k not in len_dic:
            len_dic[k] = getOneLen(v)
    return len_dic

def getOneLen(one_dic):
    length = 0
    for k, v in one_dic.items():
        for s in k:
            # length += 2 * v
            if s >= '0' and s <= '9':
                length += v
            else:
                length += 2 * v
    return length

def getIntersection(dic_a, dic_b):
    inter_list = []
    for k, v in dic_a.items():
        if k in dic_b:
            inter_list.append(k)
    return inter_list

def getDF(t, all_dic_d):
    count = 0
    for k, v in all_dic_d.items():
        if t in v:
            count += 1
    return count

def getAvdl(data_w_d):
    n = len(data_w_d)
    total_len = 0
    for k, v in data_w_d.items():
        total_len += getOneLen(v)
    return float(total_len / n) 

def getSimilarity(all_dic_d, q, len_dic):
    similarity_list = []
    avdl = getAvdl(all_dic_d)
    n = len(all_dic_d)
    cnt = 0
    for k, v in all_dic_d.items():
        # print(cnt)
        inter_list = getIntersection(v, q)
        d = len_dic[k]
        down = float(1 - s + s * d / avdl)
        similarity = 0
        for t in inter_list:
            c_d = v[t]
            c_q = q[t]
            df = getDF(t, all_dic_d)
            idf = math.log((n + 1) / df)
            up = 1 + math.log(1 + math.log(c_d))
            similarity += up / down * c_q * idf
        similarity_list.append(similarity)
        cnt += 1
    return similarity_list



if __name__ == '__main__':
    data = getData("199801_clear.txt")
    data_w = data[0]
    data_p = data[1]
    all_dic = getAllDic(data_w)
    flag = 0
    len_dic = getLenDic(all_dic)
    # print(len_dic)
    start_1 = time.time()
    start_2 = time.process_time()
    for k, v in all_dic.items():
        if flag >= 1:
            break
        flag += 1
        temp_dic = copy.deepcopy(all_dic)
        q = temp_dic.pop(k)
        similarity_list = getSimilarity(temp_dic, q, len_dic)
        # print(similarity_list)
    pool.close()
    pool.join()
    end_2 = time.process_time()
    end_1 = time.time()
    print(end_1 - start_1)
    print(end_2 - start_2)

        