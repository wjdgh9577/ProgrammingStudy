import numpy as np

def solution(gems):
    answer = []
    
    gemset = set()
    for gem in gems:
        gemset.add(gem)
    v = len(gemset)   #최소
    V = len(gems)     #최대
    gemset.clear()
    
    table = np.array([0]*V)
    for i in range(V):
        for j in range(i, V):
            gemset.add(gems[j])
            if len(gemset) == v:
                table[i] = j-i+1
                break
        gemset.clear()
    
    m = np.where(table == np.min(table[table>0]))
    
    answer.append(m[0][0]+1)
    answer.append(m[0][0]+table[m[0][0]])
    
    return answer
