from itertools import permutations

def solution(user_id, banned_id):
    answer = 0
    possible = list(permutations(user_id, len(banned_id)))
    result = set()
    for l in possible:
        isSame = True
        for i in range(len(l)):
            if len(l[i]) == len(banned_id[i]):
                ui = l[i]
                bi = banned_id[i]
                for j in range(len(ui)):
                    if ui[j] != bi[j] and bi[j] != '*':
                        isSame = False
                        break
                if not isSame:
                    break
            else:
                isSame = False
                break
        if isSame:
            result.add(frozenset(l))
    answer = len(result)
    
    return answer
