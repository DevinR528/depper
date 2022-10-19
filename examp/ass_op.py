def loop_func():
    n = 10
    A = [[0 for _ in range(11)] for _ in range(11)]
    for i in range(10):
        for j in range(1):
            A[i+1][j] += A[i][j] + 1

ListComp(
    elt=ListComp(
        elt=Constant(value=0),
        generators=[
            comprehension(
                target=Name(id='_', ctx=Store()),
                iter=Call(
                    func=Name(id='range', ctx=Load()),
                    args=[Constant(value=11)],
                    keywords=[]
                ),
                ifs=[],
                is_async=0
            )
        ]
    ),
    generators=[
        comprehension(
            target=Name(id='_', ctx=Store()),
            iter=Call(func=Name(id='range', ctx=Load()), args=[Constant(value=11)], keywords=[]),
            ifs=[],
            is_async=0
        )
    ]
)

If(
    test=Compare(
        left=Name(id='n', ctx=Load()),
        ops=[Gt()],
        comparators=[Constant(value=5)]
    ),
    body=[Assign(
        targets=[
            Subscript(
                value=Subscript(
                    value=Name(id='A', ctx=Load()),
                    slice=BinOp(left=Name(id='i', ctx=Load()),
                    op=Add(),
                    right=Constant(value=1)),
                    ctx=Load()
                ),
                slice=Name(id='j', ctx=Load()),
                ctx=Store()
            )
        ],
        value=BinOp(
            left=Subscript(
                value=Subscript(
                    value=Name(id='A', ctx=Load()),
                    slice=Name(id='i', ctx=Load()),
                    ctx=Load()
                ),
                slice=Name(id='j', ctx=Load()),
                ctx=Load()
            ),
            op=Add(),
            right=Constant(value=1)
        )
    )],
    orelse=[
        If(test=Compare(
            left=Name(id='n', ctx=Load()),
            ops=[LtE()],
            comparators=[Constant(value=2)]),
            body=[
                Assign(targets=[
                    Subscript(
                        value=Subscript(
                            value=Name(id='A', ctx=Load()),
                            slice=Name(id='i', ctx=Load()),
                            ctx=Load()
                        ),
                        slice=BinOp(
                            left=Name(id='j', ctx=Load()),
                            op=Add(),
                            right=Constant(value=1)
                        ),
                        ctx=Store()
                    )
                ],
                value=Subscript(
                    value=Subscript(
                        value=Name(id='A', ctx=Load()),
                        slice=Name(id='i', ctx=Load()),
                        ctx=Load()
                    ),
                    slice=Name(id='j', ctx=Load()),
                    ctx=Load()
                )
            )],
            orelse=[Assign(
                targets=[
                    Subscript(
                        value=Subscript(
                            value=Name(id='A', ctx=Load()),
                            slice=Name(id='i', ctx=Load()),
                            ctx=Load()
                        ),
                        slice=Name(id='j', ctx=Load()),
                        ctx=Store()
                    )
                ],
                value=BinOp(
                    left=Subscript(
                        value=Subscript(
                            value=Name(id='A', ctx=Load()),
                            slice=Name(id='i',ctx=Load()),
                            ctx=Load()
                        ),
                        slice=Name(id='j', ctx=Load()),
                        ctx=Load()
                    ),
                    op=Add(),
                    right=Constant(value=2)
                )
            )]
        )
    ]
)

