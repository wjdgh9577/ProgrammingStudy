def distance(finger, number):
    if finger == 0:
        fin_x = 1
        fin_y = 3
    elif finger == '*':
        fin_x = 0
        fin_y = 3
    elif finger == '#':
        fin_x = 2
        fin_y = 3
    else:
        fin_x = (finger-1)%3
        fin_y = (finger-1)//3
    
    num_x = 1
    if number == 0:
        num_y = 3
    else:
        num_y = (number-1)//3
    
    return abs(fin_x-num_x) + abs(fin_y-num_y)

def solution(numbers, hand):
    answer = ''
    left = '*'
    right = '#'
    isRightHand = True
    if hand == 'left':
        isRightHand = False
    
    for number in numbers:
        if number in [1, 4, 7]:
            answer += 'L'
            left = number
        elif number in [3, 6, 9]:
            answer += 'R'
            right = number
        else:
            lton = distance(left, number)
            rton = distance(right, number)
            print(lton, rton)
            if lton < rton:
                answer += 'L'
                left = number
            elif lton > rton:
                answer += 'R'
                right = number
            else:
                if isRightHand:
                    answer += 'R'
                    right = number
                else:
                    answer += 'L'
                    left = number
    
    return answer
