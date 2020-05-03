# ***************************************************************************
# https://www.acmicpc.net/problem/10817
#
# 문제 : 세 정수 A, B, C가 주어진다. 이때, 두 번째로 큰 정수를 출력하는
#        프로그램을 작성하시오. 
# 입력 : 첫째 줄에 세 정수 A, B, C가 공백으로 구분되어 주어진다.
#        (1 ≤ A, B, C ≤ 100)
# 출력 : 두 번째로 큰 정수를 출력한다.
# ***************************************************************************

A, B, C = map(int, input().split())

if A >= 1 and B >= 1 and C >= 1 and A <= 100 and B <= 100 and C <= 100:
    max = max(A, B, C)
    min = min(A, B, C)
    if A == max:
        if B == min:
            print(C)
        else:
            print(B)
    elif B == max:
        if A == min:
            print(C)
        else:
            print(A)
    else:
        if A == min:
            print(B)
        else:
            print(A)
