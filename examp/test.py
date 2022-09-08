def print_matrix(matrix):
    print('[')
    for el in matrix:
        print(el, ',')
    print(']')


def loop_func():
    A = [[0 for _ in range(11)] for _ in range(11)]
    for i in range(10):
        for j in range(10):
            A[i+1][j] = A[i][j] + 1

loop_func()
