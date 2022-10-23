from ast import BinOp, parse
from enum import Enum
from typing import List, Mapping, Optional, Tuple
from typing_extensions import Self
from expr_info import BinOpKind, BinaryOp, ForStmt, Expression, IfStmt, Stmt, StmtKind


class DepKind(Enum):
    """
    The different kinds of dependency.
    """

    # Start of dependency graph
    START = 0

    # The memory location is written to then read from
    TRUE = 1

    # The memory location is read from then written to.
    ANTI = 2

    # The memory location is written to twice followed by a read later or
    # there is no dependence and the output dep doesn't matter.
    OUTPUT = 3


class DepNode:
    name: str
    kind: DepKind
    children: List[Self]

    def __init__(self, name: str, kind: DepKind) -> None:
        self.name = name
        self.kind = kind
        self.children = []

    def __repr__(self) -> str:
        return (
            '{'
            + f'"tag":"DepNode","name":{self.name},"kind":"{self.kind}","kids":{self.children}'
            + '}'
        )


class DepGraph:
    root: DepNode

    def __init__(self) -> None:
        self.root = DepNode(0, DepKind.START)

    def __repr__(self) -> str:
        return '{' + f'"tag":"DepGraph", "root":{self.root}' + '}'

    def add_read(self, expr: Expression):
        pass

    def add_write(self, expr: Expression):
        pass


class CtrlNode:
    name: str
    edge: Tuple[bool, Expression]
    block: List[Stmt]
    children: List[Self]

    def __init__(
        self,
        name: str,
        parents: List[Self] = [],
        edge: Optional[Tuple[bool, Expression]] = None,
    ) -> None:
        self.name = name
        self.block = []
        self.edge = edge
        self.children = []
        self.parents = parents

    def __repr__(self) -> str:
        edge = ''
        if self.edge is not None:
            ed = 'true' if self.edge[0] else 'false'
            ed2 = self.edge[1] if self.edge[1] else 'null'
            edge = f'{ed},{ed2}'
        return (
            '{'
            + f'"tag":"CtrlNode","name":{self.name},"kids":{self.children},'
            + f'"block":{self.block},"edge":[{edge}]'
            + '}'
        )


class CtrlGraph:
    root: CtrlNode
    current: List[CtrlNode]
    count: int = 0

    def __init__(self) -> None:
        self.root = CtrlNode(self.count)
        self.current = [self.root]

    def __repr__(self) -> str:
        return '{' + f'"tag":"CtrlGraph", "root":{self.root}' + '}'

    def branch_if(self, ctrl_flow: IfStmt):
        self.count += 1
        currents = self.current

        tru = CtrlNode(self.count, currents, (True, ctrl_flow.cond))
        for c in self.current:
            c.children.append(tru)

        self.current = [tru]
        for s in ctrl_flow.then:
            match s.kind:
                case StmtKind.IF:
                    self.branch_if(s.value)
                case StmtKind.FOR:
                    self.branch_for(s.value)
                case StmtKind.ASSIGN:
                    self.add_curr_blk(s)

        self.current = currents
        # TODO: elifs...

        self.count += 1
        fals = CtrlNode(self.count, currents, (False, ctrl_flow.els))
        for c in self.current:
            c.children.append(fals)

        self.current = [fals]
        for s in ctrl_flow.then:
            match s.kind:
                case StmtKind.IF: self.branch_if(s.value)
                case StmtKind.FOR: self.branch_for(s.value)
                case StmtKind.ASSIGN: self.add_curr_blk(s)

        # Merge node, the join of if/else
        self.count += 1
        new = CtrlNode(self.count, [tru, fals], None)
        tru.children.append(new)
        fals.children.append(new)
        self.current = [new]

    def branch_for(self, ctrl_flow: ForStmt):
        self.count += 1
        currents = self.current
        # test_expr = Expression.from_for(BinOpKind.LT, ctrl_flow.index_var.name, ctrl_flow.loop_bound.stop)
        test_expr = None
        loop = CtrlNode(self.count, currents, (True, test_expr))
        for c in currents:
            c.children.append(loop)

        self.current = [loop]
        for s in ctrl_flow.body:
            match s.kind:
                case StmtKind.IF: self.branch_if(s.value)
                case StmtKind.FOR: self.branch_for(s.value)
                case StmtKind.ASSIGN: self.add_curr_blk(s)

        self.current = currents

        self.count += 1
        skip = CtrlNode(self.count, currents, (False, test_expr))
        for c in self.current:
            c.children.append(skip)

        self.count += 1
        new = CtrlNode(self.count, [loop, skip])
        loop.children.append(new)
        skip.children.append(new)
        self.current = [new]


    def add_curr_blk(self, stmt: Stmt):
        for c in self.current:
            c.block.append(stmt)


class NameMap(dict):
    '''
    `VarName` to `Expression` mapping for variable tracking and constant folding.
    '''

    def __init__(self) -> None:
        return super().__init__()


class LoopInfo:
    loop_level: Mapping[ForStmt, int]
    for_stmt: Mapping[Expression, ForStmt]

    def __init__(self) -> None:
        self.loop_level = 0
        self.for_stmt = {}

    def __repr__(self) -> str:
        return '{' + '"tag":"LoopInfo"' + '}'

    def add_loop(self, loop: ForStmt, lvl: int):
        pass
