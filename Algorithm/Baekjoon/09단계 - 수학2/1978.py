# ***************************************************************************
# https://www.acmicpc.net/problem/1978
#
# 문제 : 주어진 수 N개 중에서 소수가 몇 개인지 찾아서 출력하는 프로그램을
#        작성하시오.
# 입력 : 첫 줄에 수의 개수 N이 주어진다. N은 100이하이다.
#        다음으로 N개의 수가 주어지는데 수는 1,000 이하의 자연수이다.
# 출력 : 주어진 수들 중 소수의 개수를 출력한다.
# ***************************************************************************

from math import ceil, sqrt

def isPrime(N):
    if N == 1:
        return 0
    if N > 2:
        for i in range(2, ceil(sqrt(N)+1)):
            if N%i == 0:
                return 0
    return 1

N = int(input())
count = 0
for i in map(int, input().split()):
    count += isPrime(i)
print(count)
