'''
***************************************************
<input data format>
'u#.base'
[user_id]\t[item_id]\t[rating]\t[time_stamp]\n
[user_id]\t[item_id]\t[rating]\t[time_stamp]\n
[user_id]\t[item_id]\t[rating]\t[time_stamp]\n
[user_id]\t[item_id]\t[rating]\t[time_stamp]\n
'u#.test'
[user_id]\t[item_id]\t[rating]\t[time_stamp]\n
[user_id]\t[item_id]\t[rating]\t[time_stamp]\n
[user_id]\t[item_id]\t[rating]\t[time_stamp]\n
[user_id]\t[item_id]\t[rating]\t[time_stamp]\n
.
.
.

<output data format of input#>
'u#.base_prediction.txt'
[user_id]\t[item_id]\t[rating]\n
[user_id]\t[item_id]\t[rating]\n
[user_id]\t[item_id]\t[rating]\n
[user_id]\t[item_id]\t[rating]\n
.
.
.
***************************************************
'''

import sys
from math import sqrt


# input file에 대한 정보를 읽고 필요한 형식의 데이터로 반환한다.
def init():
    # Exception
    if len(sys.argv) != 3:
        print("Input \"recommender.py (u#.base) (u#.test)\"")
        exit(1)

    base, test = sys.argv[1:]

    f = open(base, "r")
    lines = f.readlines()
    base = dict()
    for line in lines:
        user_id, item_id, rating, _ = map(int, line.split())
        if user_id in base:
            base[user_id][item_id] = rating
        else:
            base[user_id] = {item_id: rating}
    f.close()

    f = open(test, "r")
    lines = f.readlines()
    test = dict()
    for line in lines:
        user_id, item_id, _, _ = map(int, line.split())
        if user_id in test:
            test[user_id].append(item_id)
        else:
            test[user_id] = [item_id]
    f.close()

    return base, test, sys.argv[1]


# 두 사용자가 공통으로 평가한 item에 대한 rating의 평균을 반환한다.
# d: 사용자가 평가한 item과 rating의 dictionary {item1: rating1, item2: rating2, ...}
# s: 두 사용자가 공통으로 평가한 item set
def mean(d, s):
    sum = 0
    for i in s:
        sum += d[i]
    m = sum / len(s)
    return m


# 피어슨 유사도를 계산하여 반환한다.
# d1: 사용자1이 평가한 item과 rating의 dictionary
#       {item1: rating1, item2: rating2, ...}
# d2: 사용자2가 평가한 item과 rating의 dictionary
#       {item1: rating1, item2: rating2, ...}
# s: 두 사용자가 공통으로 평가한 item set
def pearson(d1, d2, s):
    # 공통으로 평가한 item이 없는 경우 유사도는 0
    if len(s) == 0:
        return 0

    m1 = mean(d1, s)
    m2 = mean(d2, s)
    a1 = a2 = a3 = 0

    for i in s:
        t1 = d1[i] - m1
        t2 = d2[i] - m2
        a1 += t1 * t2
        a2 += t1 ** 2
        a3 += t2 ** 2

    a2 = sqrt(a2)
    a3 = sqrt(a3)

    # 분모가 0이 되는 것을 방지하기 위해 1을 더한다.
    sim = a1 / (a2 * a3 + 1)

    return sim


# 모든 사용자간의 유사도를 나타내는 table을 반환한다.
# base: 모든 사용자의 item에 대한 rating을 가진 dictionary
#       {id1: {item1: rating1, ...}, id2: {item1: rating1, ...}, ...}
def similarity(base):
    # 사용자의 id의 list
    user_ids = list(base.keys())

    table = [[0] * len(user_ids)] * len(user_ids)

    for i in range(len(user_ids)):
        for j in range(i, len(user_ids)):
            # user#: user id
            user1 = user_ids[i]
            user2 = user_ids[j]

            # item2rating#: base dictionary에서 user id로 참조한 dictionary
            # item id로 rating을 참조할 수 있음
            item2rating1 = base[user1]
            item2rating2 = base[user2]

            # inter: 두 사용자가 공통으로 평가한 item set
            set1 = set(item2rating1.keys())
            set2 = set(item2rating2.keys())
            inter = set1 & set2

            sim = pearson(item2rating1, item2rating2, inter)
            table[i][j] = table[j][i] = sim

    return table


# 사용자간의 유사도를 통해 rating을 예측한다.
# base: 모든 사용자의 item에 대한 rating을 가진 dictionary
#       {id1: {item1: rating1, ...}, id2: {item1: rating1, ...}, ...}
# test: 사용자의 예측할 item list
#       {id1: [item1, item2, ...], id2: [item1, item2, ...], ...}
# table: 모든 사용자간의 유사도를 나타낸 표
def predict(base, test, table):
    # index를 통해 id를 참조할 수 있는 list
    index2id = list(base.keys())
    # id를 통해 index를 참조할 수 있는 dictionary
    id2index = {index2id[i]: i for i in range(len(index2id))}

    result = []

    for id, items in test.items():
        for item in items:
            a1 = a2 = 0
            for i in range(len(index2id)):
                if item in base[index2id[i]]:
                    sim = table[id2index[id]][i]
                    r = base[index2id[i]][item]
                    a1 += sim * r
                    a2 += sim

            if a2 == 0:
                # 예측할 item에 대한 평가가 없는 경우 사용자의 모든 rating의 평균으로 예측한다.
                rating = round(sum(base[id].values()) / len(base[id]))
            else:
                rating = round(a1 / a2)

            # 예측한 rating이 범위(1~5)를 벗어난 경우 조정해준다.
            if rating < 1:
                rating = 1
            elif rating > 5:
                rating = 5

            result.append((id, item, rating))

    return result


# 예측한 결과를 텍스트 파일로 출력한다.
def printResult(result, text):
    f = open(text + "_prediction.txt", "w")
    f.writelines(str(id) + "\t" + str(item) + "\t" + str(rating) + "\n" for id, item, rating in result)
    f.close()
    return


if __name__ == "__main__":
    base, test, text = init()
    table = similarity(base)
    result = predict(base, test, table)
    printResult(result, text)
