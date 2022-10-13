
def loop_func():
    U = [0 for _ in range(300)]
    V = [0 for _ in range(300)]
    W = [0 for _ in range(300)]

    for i in range(100):
        ki = i
        for j in range(0, 300, 3):
            ki += 2
            U[j] = U[j] * W[ki]
            V[j+3] = U[j] * W[ki]


def into_this():
    U = [0 for _ in range(300)]
    V = [0 for _ in range(300)]
    W = [0 for _ in range(300)]

    for i in range(100):
        ki = i
        for j in range(100):
            U[3 * j - 2] = U[3 * j - 2] * W[ki + 2 * j]
            V[3 * j + 1] = U[3 * j - 2] * W[ki + 2 * j]
        ki += 200
        j = 300
