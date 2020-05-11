def solution(board, moves):
    basket = []
    top = 0
    answer = 0
    
    for i in moves:
        for j in range(len(board)):
            doll = board[j][i-1]
            if doll != 0:
                if len(basket) != 0 and basket[len(basket)-1] == doll:
                    basket.pop()
                    answer += 2
                else:
                    basket.append(doll)
                board[j][i-1] = 0
                break
    
    return answer
