# -*- coding: utf8 -*-
import numpy as np
import time

# バブルソート。
# 左右の値を比較。
# 変更の必要がなくなるまで行う。
# コードを見たらわかるので、見やすい。
# 速度は気にしないときは良さそう。
def BubbleSort(arr):
    change = True
    while change:
        change = False
        for i in range(len(arr) - 1):
            #　右側のほうが小さいので交換。
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                change = True
    return arr

# クイックソート。
# 基準値を決めて、基準値から見た大小の2つの配列に分ける。
# 分けたグループで再帰的に処理を行う。
# 早いけど、メモリを食いそう。
# データ数が膨大な時はクイックソートがよさそう。
def QuickSort(arr):
    left = []
    right = []

    if len(arr) <= 1:
        return arr

    # とりあえず最初のデータを設定。
    pivot = arr[0]
    pivot_count = 0

    # 基準値から大小の配列を設定。
    for ele in arr:
        if ele < pivot:
            left.append(ele)
        elif ele > pivot:
            right.append(ele)
        else:
            pivot_count += 1

    left = QuickSort(left)
    right = QuickSort(right)
    
    # 左右の配列と基準値を返す。基準値の場合はカウント分。
    return left + [pivot] * pivot_count + right

# マージソート。
# ソート済みの2つの配列をソートする。
# メモリ食いそう。
# バブルソートが遅いと感じ、データ数がそれほど多くないときに使えそう。
# 2つの配列をマージするときはこっちでしょう。
def MergeSort(arr):
    length = len(arr)
    # 1だとそのまま配列を返す。
    if (length == 1):
        return arr
    else:
        # 半分より左。
        left  = MergeSort(arr[:length//2])
        # 半分より右。
        right = MergeSort(arr[length//2:])

        return np.array(Merge(left, right))

def Merge(arr1, arr2):
    lst = []
    while(True):
        len1 = len(arr1)
        len2 = len(arr2)
        # 終わり。
        if (len1==0 and len2==0):
            return lst
        # 先頭をlistに追加。
        elif (len1==0): 
            lst.append(arr2[0])
            arr2 = arr2[1:]
        elif (len2==0):
            lst.append(arr1[0])
            arr1 = arr1[1:]
        # 小さいほうを入れる。
        elif (arr1[0] < arr2[0]):
            lst.append(arr1[0])
            arr1 = arr1[1:]
        else:
            lst.append(arr2[0])
            arr2 = arr2[1:]


#array = [3,4,9,1,5,2,7,8,6]
MAX_NUM = 1000

# バブルソート。
array = np.random.randint(0,MAX_NUM,MAX_NUM)
start_time = time.time()
BubbleSort(array)
end_time = time.time()
print(u"バブルソート時間:%f" % (end_time - start_time))

# クイックソート。
array = np.random.randint(0,MAX_NUM,MAX_NUM)
start_time = time.time()
QuickSort(array)
end_time = time.time()
print(u"クイックソート時間:%f" % (end_time - start_time))

# マージソート。
array = np.random.randint(0,MAX_NUM,MAX_NUM)
start_time = time.time()
MergeSort(array)
end_time = time.time()
print(u"マージソート時間:%f" % (end_time - start_time))
