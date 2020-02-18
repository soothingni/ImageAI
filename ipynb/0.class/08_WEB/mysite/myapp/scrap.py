import sys
T = int(sys.stdin.readline().rstrip())
for _ in range(T):
    N, K = map(int, sys.stdin.readline().rstrip().split())
    D = list(map(int, sys.stdin.readline().rstrip().split()))
    time_dict = {'1': D[0]}
    for _ in range(K):
        a, b = sys.stdin.readline().rstrip().split()
        temp = time_dict[a] + D[int(b) - 1]
        if b in time_dict and temp < time_dict[b]: continue
        else: time_dict[b] = temp
    W = sys.stdin.readline().rstrip()
    print(time_dict[W])