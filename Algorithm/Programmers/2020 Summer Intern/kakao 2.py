def solution(expression):
    answer = 0
    order = ['+-*', '-+*', '+*-', '-*+', '*+-', '*-+']
    result = []
    
    el = []
    number = 0
    for e in expression:
        if e.isdigit():
            number = number*10 + int(e)
        else:
            el.append(number)
            number = 0
            el.append(e)
    el.append(number)
    
    stack = []
    for o in order:
        l = el.copy()
        for e in o:
            while len(l) > 0:
                n = l.pop(0)
                if n == e:
                    if e == '+':
                        n = stack.pop() + l.pop(0)
                    elif e == '-':
                        n = stack.pop() - l.pop(0)
                    elif e == '*':
                        n = stack.pop() * l.pop(0)
                stack.append(n)
            l = stack.copy()
            stack = []
        result.append(abs(l.pop()))
                        
    
    answer = max(result)
    return answer
