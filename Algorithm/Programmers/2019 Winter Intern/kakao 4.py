#sol1
def solution(k, room_number):
    answer = []
    
    dic = {}
    for i in room_number:
        p = i
        visit = [p]
        while p in dic:
            visit.append(p)
            p = dic[p]
        answer.append(p)
        dic[p] = p+1
        for v in visit:
            dic[v] = p+1
            
    return answer
'''
#sol2
import sys
sys.setrecursionlimit(10000000) 
def find(number, rooms):
    if number not in rooms:
        rooms[number] = number + 1
        return number
    empty = find(rooms[number], rooms)
    rooms[number] = empty + 1
    return empty


def solution(k, room_number):
    answer = []
    rooms = {}

    for number in room_number:
        emptyroom = find(number,rooms)
        answer.append(emptyroom)
    return answer
'''
'''
#time over
def solution(k, room_number):
    answer = []
    
    dic = {}
    for i in room_number:
        if i not in answer:
            answer.append(i)
            dic[i] = i+1
        else:
            p = dic[i]
            while p in answer:
                p = dic[p]
            answer.append(p)
            dic[p] = p+1
            dic[i] = p+1
    
    return answer
'''
'''
#time over
def solution(k, room_number):
    answer = []
    
    for i in room_number:
        while i in answer:
            i += 1
        answer.append(i)
    
    return answer
'''
