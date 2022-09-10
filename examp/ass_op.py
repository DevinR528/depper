def loop_func():
    n = 10
    A = [[0 for _ in range(11)] for _ in range(11)]
    for i in range(10):
        for j in range(1):
            A[i+1][j] += A[i][j] + 1


Assign(
    targets=[
        Subscript(
            value=Subscript(
                value=Name(id='A'),
                slice=Index(value=BinOp(left=Name(id='i'), op=Add(),
                            right=Constant(value=1, kind=None))),
            ),
            slice=Index(value=Name(id='j')),
        )
    ],
    value=BinOp(
        left=Subscript(
            value=Subscript(value=Name(id='A'), slice=Index(
                value=Name(id='i'))
            ),
            slice=Index(value=Name(id='j')),
        ),
        op=Add(),
        right=Constant(value=1, kind=None)
    ),
    type_comment=None
)
