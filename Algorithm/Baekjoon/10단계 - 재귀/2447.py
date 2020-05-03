# ***************************************************************************
# https://www.acmicpc.net/problem/2447
#
# 문제 : 재귀적인 패턴으로 별을 찍어 보자. N이 3의 거듭제곱(3, 9, 27, ...)이라고
#        할 때, 크기 N의 패턴은 N×N 정사각형 모양이다.
#        크기 3의 패턴은 가운데에 공백이 있고, 가운데를 제외한 모든 칸에 별이
#        하나씩 있는 패턴이다.
#         ***
#         * *
#         ***
#        N이 3보다 클 경우, 크기 N의 패턴은 공백으로 채워진 가운데의
#        (N/3)×(N/3) 정사각형을 크기 N/3의 패턴으로 둘러싼 형태이다.
#        예를 들어 크기 27의 패턴은 예제 출력 1과 같다.
# 입력 : 첫째 줄에 N이 주어진다. N은 3의 거듭제곱이다.
#        즉 어떤 정수 k에 대해 N=3k이며, 이때 1 ≤ k < 8이다.
# 출력 : 첫째 줄부터 N번째 줄까지 별을 출력한다.
# ***************************************************************************

'''
import sys
write = sys.stdout.write

def star(row, col):
    while row != 0:
        if row%3 == 1 and col%3 == 1:
            write(" ")
            return
        row = row//3
        col = col//3
    write("*")

N = int(input())
for row in range(N):
    for col in range(N):
        star(row, col)
    write("\n")
'''
def star(n, row, col):
    if n == 1:
        canvas[row][col] = "*"
        return
    
    for i in range(3):
        for j in range(3):
            if i != 1 or j != 1:
                star(n//3, row + n//3 * i, col + n//3 * j)

N = int(input())
canvas = [[" "]*N for _ in range(N)]

star(N, 0, 0)

for l in canvas:
    print("".join(l))
