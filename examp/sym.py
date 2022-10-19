class Foo:
    def __init__(self) -> None:
        pass


def loop_func():
    n = 10
    a = 'hello'
    m = (10 / 2)
    o = loop_func(10, 'hello')
    os = [0, 1, 2]
    A = [0 for _ in range(11)]
    # A = [[0 for _ in range(11)] for _ in range(11)]
    for i in range(10):
        for j in range(n):
            if n > 5:
                A[i + 1][j] = A[i][j] + 1
            elif n <= 2:
                A[i][j + 1] = A[i][j]
            elif n == 2:
                A[i][j + 1] = A[i][j]
            else:
                A[i][j] = A[i][j] + 2

# def loop_func():
#     n = 10
#     A = [[0 for _ in range(11)] for _ in range(11)]
#     for i in range(10):
#         for j in range(n):
#             A[i][j] = A[i + 1][j] + 1
