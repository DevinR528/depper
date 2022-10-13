from enum import Enum
from typing import List, Optional
from typing_extensions import Self
from loop_info import Assignment, Expression, LoopDepInfo, Bound, SubScriptIdx


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
    children: List[Self]
    name: str
    kind: DepKind

    loop: Optional[LoopDepInfo]

    expr: Expression
    assign: Assignment

    def __init__(
        self, name: str, kind: DepKind, expr: Expression, assign: Assignment, loop=None
    ) -> Self:
        self.children = []
        self.name = name
        self.kind = kind

        self.expr = expr
        self.assign = assign
        self.loop = loop


class DepGraph:
    root: DepNode

    def __init__(self) -> Self:
        self.root = DepNode('start', DepKind.START)


class NameMap(dict):
    def __init__(self) -> Self:
        return super().__init__()


def dumb():
    m = NameMap()
    m.get
