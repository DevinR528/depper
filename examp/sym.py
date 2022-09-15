class Foo:
    def __init__(self) -> None:
        pass


def loop_func():
    n = 10
    m = (10 / 2)
    o = loop_func()
    os = []
    A = [[0 for _ in range(11)] for _ in range(11)]
    for i in range(10):
        for j in range(n):
            A[i+1][j] = A[i][j] + 1
