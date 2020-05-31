'''
***************************************************
<input data format>
[object_id_1]\t[x_coordinate]\t...\t[y_coordinate]\n
[object_id_2]\t[x_coordinate]\t...\t[y_coordinate]\n
[object_id_3]\t[x_coordinate]\t...\t[y_coordinate]\n
[object_id_4]\t[x_coordinate]\t...\t[y_coordinate]\n
.
.
.

<output data format of input#>
'input#_cluster_0.txt'
[object_id]\n
[object_id]\n
...
'input#_cluster_1.txt'
[object_id]\n
[object_id]\n
...
'input#_cluster_n-1.txt'
[object_id]\n
[object_id]\n
...
.
.
.
***************************************************
'''

import sys
sys.setrecursionlimit(2000)
from math import sqrt

# input file에 대한 정보를 읽고 필요한 형식의 데이터로 반환한다.
# dataset은 object_id, x_coordinate, y_coordinate의 배열이다.
def init():
    # Exception
    if len(sys.argv) != 5:
        print("Input \"clustering.py (input file) (n) (Eps) (MinPts)\"")
        exit(1)

    input_text, n, eps, minpts = sys.argv[1:]

    f = open(input_text, "r")
    lines = f.readlines()
    dataset = []
    for line in lines:
        id, x, y = line.split()
        dataset.append([int(id), float(x), float(y)])
    f.close()

    return input_text[:-4], int(n), float(eps), int(minpts), dataset

# DBSCAN 알고리즘을 구현한 함수
# core point일 경우 reachable points에 대해 각각 재귀호출을 수행한다.
# core : 현재 point의 object_id, x_coordinate, y_coordinate에 대한 정보가 담겨있다.
# eps : neighbor point를 정의하는 최대 거리
# minpts : core point를 만족하는 최소 neighbor 수
# cluster : 현재 cluster의 number
# clusters : 모든 cluster의 정보가 담겨있는 dictionary
# dataset : 모든 object의 정보가 담겨있는 list
# depth : 현재 재귀함수의 깊이. depth == 0일 경우 root.
def DBSCAN(core, eps, minpts, cluster, clusters, dataset, depth):
    # 이미 탐색한 point일 경우
    for ids in clusters.values():
        if core[0] in ids:
            return

    id_c, x_c, y_c = core
    reachable = []
    # 모든 point와의 거리를 계산하여 neighbor points를 탐색
    for border in dataset:
        id_b, x_b, y_b = border
        distance = sqrt((x_b-x_c)**2 + (y_b-y_c)**2)
        if distance < eps:
            reachable.append(border)

    if len(reachable) >= minpts:  # core point
        if cluster in clusters:
            clusters[cluster].add(id_c)
        else:
            clusters[cluster] = set([id_c])

        # 각각의 neighbor point에 대해 재귀호출
        for border in reachable:
            DBSCAN(border, eps, minpts, cluster, clusters, dataset, depth+1)

    else:   #border point or outlier
        # root가 border point 또는 outlier일 경우 cluster를 생성하지 않음
        if depth == 0:
            return

        if cluster in clusters:
            clusters[cluster].add(id_c)
        else:
            clusters[cluster] = set([id_c])

if __name__ == "__main__":
    input_text, n, eps, minpts, dataset = init()
    cluster = 0
    clusters = dict()

    # 모든 points에 대해서 탐색(complete method)
    for core in dataset:
        DBSCAN(core, eps, minpts, cluster, clusters, dataset, 0)
        cluster += 1

    # clustering 후 cluster의 수가 n보다 클 경우 size가 작은 순으로 제거
    m = len(clusters.keys())
    for i in range(m-n):
        key = 0
        min = len(dataset)
        for k, v in clusters.items():
            if len(v) < min:
                key = k
                min = len(v)
        del clusters[key]

    # 결과를 input#_cluster_i.txt로 출력
    num = 0
    for key in clusters.keys():
        f = open(input_text+"_cluster_"+str(num)+".txt", "w")
        cluster = list(clusters[key])
        f.writelines(str(id)+"\n" for id in cluster)
        f.close()
        num += 1