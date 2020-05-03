'''
***************************************************
<training data format>
[attribute_name_1]\t[attribute_name_2]\t...\t[attribute_name_n]\n
[attribute_1]\t[attribute_2]\t...\t[attribute_n]\n
[attribute_1]\t[attribute_2]\t...\t[attribute_n]\n
[attribute_1]\t[attribute_2]\t...\t[attribute_n]\n
.
.
.

<test data format>
[attribute_name_1]\t[attribute_name_2]\t...\t[attribute_name_n-1]\n
[attribute_1]\t[attribute_2]\t...\t[attribute_n-1]\n
[attribute_1]\t[attribute_2]\t...\t[attribute_n-1]\n
[attribute_1]\t[attribute_2]\t...\t[attribute_n-1]\n
.
.
.
***************************************************
'''

import sys
from math import log

# training dataset을 읽고 반환한다.
# 하나의 데이터는 dictionary로 저장되며
# {attribute1, attribute2, ... ,attributeN}의 형태를 갖는다.
# 데이터를 list로 묶어서 반환한다.
# attribute name은 별도의 list로 반환한다.
def init():
    # Exception
    if len(sys.argv) != 4:
        print("Input \"dt.py (training file) (test file) (output file)\"")
        exit(1)

    f = open(sys.argv[1], "r")  # training file
    dataset = []   # 전체 data의 list
    lines = f.readlines()
    attribute_names = lines.pop(0).split()  # attribute name list
    
    for attributes in lines:
        values = attributes.split()
        dic = {}
        for i in range(len(attribute_names)):
            dic[attribute_names[i]] = values[i]  # data 한줄에 해당
        dataset.append(dic)

    f.close()

    return dataset, attribute_names

# dataset을 attribute에 따라 분류하고, 개수를 dictionary로 저장하여 반환한다.
def CountAttributes(dataset, attribute):
    ret = {}
    for data in dataset:
        if data[attribute] in ret:
            ret[data[attribute]] += 1
        else:
            ret[data[attribute]] = 1

    return ret     # {attribute_value : count, ...}

# dataset을 attribute에 따라 분류하여 dictionary 형태로 반환한다.
def SplitDataset(dataset, attribute):
    ret = {}
    for data in dataset:
        if data[attribute] in ret:
            ret[data[attribute]].append(data)
        else:
            ret[data[attribute]] = [data]

    return ret     # {attribute_value : [data1,data2,...], ...}

# attribute에 대한 information gain(entropy)을 계산하여 반환한다.
def Info(attributes):
    total = sum(attributes.values())
    ret = 0
    for i in attributes.values():
        if i != 0:
            ret += -i/total * log(i/total, 2)

    return ret

# attribute로 split한 dataset의 information gain(entropy)을 계산하고
# gain값과 split한 dataset을 반환한다.
# gain = info - infoA
def Gain(dataset, attribute):
    info = Info(CountAttributes(dataset, attribute_names[-1]))
    infoA = 0
    total = len(dataset)
    subsets = SplitDataset(dataset, attribute)
    for subset in subsets.values():
        infoA += len(subset)/total * Info(CountAttributes(subset, attribute_names[-1]))
    
    return info - infoA, subsets

# tree를 구성하는 node class를 선언한다.
# node class는 해당 node의 attribute name data를 가지고 있고
# attribute를 key value로 child node를 참조한다.
class Node:
    def __init__(self, attribute):
        self.attribute = attribute  # attribute name이 할당
        self.label = None
        self.childs = {}     # {attribute_value : child_node, ...}

    # 각 node별로 최적의 label을 계산하는 함수이다.
    def Label(self, dataset, attribute):
        split = CountAttributes(dataset, attribute)
        count = 0
        for l, c in split.items():
            if c > count:
                count = c
                self.label = l

# decision tree를 build하는 함수이다.
# attribute selection measure : information gain
# 각 attribute로 split 했을 때의 gain값을 계산하여 최적의 attribute를 채택한다.
# node마다 최적의 label을 계산한다.
# 분류에 사용된 attribute는 list에서 제거하여 재사용을 방지한다.
# gain값이 0인 경우는 더이상 분류할 attribute가 없거나 entropy가 0인 경우이므로
# child node의 생성을 중단한다.
# 함수를 재귀호출 할 때 attribute list를 깊은 복사하여 함수간의 독립성을 유지한다.
def BuildTree(dataset, attribute_names, parent):
    gain = 0
    for an in attribute_names[:-1]:
        g, s = Gain(dataset, an)
        if g > gain:
            attribute = an
            gain = g
            split = s

    parent.Label(dataset, attribute_names[-1])
    if gain == 0:   # len(attribute_name) == 1 or info == 0
        return

    attribute_names.remove(attribute)
    parent.attribute = attribute
    for a, s in split.items():
        parent.childs[a] = Node(None)
        BuildTree(s, attribute_names.copy(), parent.childs[a])

# training한 tree를 사용하여 test를 진행하는 함수이다.
# root부터 해당 node의 attribute값을 참고하여 depth를 높인다.
# test data에 부합되는 attribute가 없는 경우 탐색을 중단하고 해당 node의
# 최적의 label을 출력한다.
def test(root, attribute_names):
    f = open(sys.argv[2], "r")    # test file
    test_dataset = []    # test data list
    lines = f.readlines()
    lines.pop(0)       # attribute name 제거
    
    for attributes in lines:
        values = attributes.split()
        dic = {}
        for i in range(len(attribute_names[:-1])):
            dic[attribute_names[i]] = values[i]
        test_dataset.append(dic)
    f.close()
    
    f = open(sys.argv[3], "w")     #result file
    f.writelines(an+"\t" for an in attribute_names)
    f.writelines("\n")
    for data in test_dataset:
        f.writelines(a+"\t" for a in data.values())
        node = root
        while len(node.childs) != 0:  # leaf node까지 탐색
            if data[node.attribute] in node.childs:
                node = node.childs[data[node.attribute]]
            else:   # leaf가 아니지만 더이상 진행할 node가 없는 경우
                break
        f.writelines(str(node.label))
        f.writelines("\n")
    f.close()

if __name__ == "__main__":
    whole_dataset, attribute_names = init()
    root = Node(None)
    BuildTree(whole_dataset, attribute_names.copy(), root)
    test(root, attribute_names)
