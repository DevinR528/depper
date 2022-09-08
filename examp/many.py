def loop_func():
    A = [[0 for _ in range(11)] for _ in range(11)]
    for i in range(10):
        for j in range(10):
            for k in range(10):
                for l in range(10):
                    for m in range(10):
                        for n in range(10):
                            A[i+1][j][k][l] = A[i][j][m][n] + 1
