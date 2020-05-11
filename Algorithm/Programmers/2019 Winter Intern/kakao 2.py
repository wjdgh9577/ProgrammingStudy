def solution(s):
    set_list = []
    new_set = []
    answer = []
    
    depth = 0
    num = 0
    for i in s:
        if i == '{':
            depth += 1
        elif i == '}':
            if depth == 2:
                new_set.append(num)
                num = 0
            else:
                set_list.append(new_set)
                new_set = []
            depth -= 1
        elif i.isdigit():
            num = 10 * num + int(i)
        elif i == ',':
            if depth == 2:
                new_set.append(num)
                num = 0
            else:
                set_list.append(new_set)
                new_set = []
    
    set_list.sort(key=lambda set: len(set))
    
    for l in set_list:
        for j in l:
            if j not in answer:
                answer.append(j)
    
    return answer
