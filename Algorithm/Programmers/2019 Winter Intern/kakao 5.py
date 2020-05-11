def isPossible(stones, k, mid):
    term = 0
    for i in stones:
        if i < mid:
            term += 1
        else:
            term = 0
        if term >= k:
            return False
    return True

def solution(stones, k):
    answer = 0
    
    M = max(stones)
    m = 1
    
    while m < M-1:
        mid = (M+m)//2
        
        if isPossible(stones, k, mid):
            m = mid
        else:
            M = mid-1
    if isPossible(stones, k, M):
        answer = M
    else:
        answer = m
    
    return answer
'''
def solution(stones, k):
    answer = 0
    
    term = 0
    isPossible = True
    for i in stones:
        term += 1
        if i != 0:
            term = 0
        elif term == k:
            isPossible = False
            break
    if isPossible:
        answer += 1
        stones = [i-1 if i != 0 else 0 for i in stones]
    
    while isPossible:
        term = 0
        isPossible = True
        for i in stones:
            term += 1
            if i != 0:
                term = 0
            elif term == k:
                isPossible = False
                break
        if isPossible:
            answer += 1
            stones = [j-1 if j != 0 else 0 for j in stones]
    
    return answer
'''
