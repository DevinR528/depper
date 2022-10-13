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

ListComp(
    elt=Constant(value=0),
    generators=[
        comprehension(target=Name(id='_', ctx=Store()),
        iter=Call(func=Name(id='range', ctx=Load()), args=[Constant(value=11)], keywords=[]),
        ifs=[],
        is_async=0)
    ]
)
