def other(amt): return range(amt)


def loop_func():
    A = [[0 for _ in range(11)] for _ in range(11)]
    for i in other(10):
        for j in range(10):
            A[i+1][j] = A[i][j] + 1
