# ***************************************************************************
# https://www.acmicpc.net/problem/9663
#
# 문제 : N-Queen 문제는 크기가 N × N인 체스판 위에 퀸 N개를 서로 공격할 수 없게 놓는 문제이다.
#       N이 주어졌을 때, 퀸을 놓는 방법의 수를 구하는 프로그램을 작성하시오.
# 입력 : 첫째 줄에 N이 주어진다. (1 ≤ N < 15)
# 출력 : 첫째 줄에 퀸 N개를 서로 공격할 수 없게 놓는 경우의 수를 출력한다.
# ***************************************************************************

def nQueen(depth, n, queens, check):
    if depth == n:
        return 1

    count = 0
    for i in range(n):
        if check[depth][i]:
            continue

        next_check = check.copy()
        

    return count

N = int(input())

queens = []
check = [[False]*N]*N

count = nQueen(0, N, queens, check)
print(count)

'''
# time over
def check(queens):
    n = len(queens)
    for i in range(n-1):
        for j in range(i+1, n):
            if j-i == abs(queens[j]-queens[i]):
                return False

    return True

def nQueen(depth, n, queens):
    if depth == n:
        if check(queens):
            return 1
        return 0

    count = 0
    for i in range(n):
        if i in queens:
            continue

        queens.append(i)
        count += nQueen(depth+1, n, queens)
        queens.pop()

    return count

N = int(input())

queens = []
count = nQueen(0, N, queens)
print(count)
'''