from ast import (
    AST, BinOp, Constant, For, Name, expr, operator, Add, BitAnd, BitOr,
    BitXor, Div, FloorDiv, LShift, RShift, Mod, Mult, MatMult, Pow,
    Sub, Invert, Not, UAdd, USub, Eq, Gt, GtE, Lt, LtE, NotEq, NotIn
)
import enum
from typing import List, Union

# fmt: off
def op_to_str(op: operator) -> str:
    """

    Return a string representing the operator.

    A string representation is not already provided in python's AST package,
    so here it is.

    ## Example
    ```py
    assert op_to_str(ast.Add()) == "+"
    ```
    """
    match op:
        case Add(): return "+"
        case BitAnd(): return "&"
        case BitOr(): return "|"
        case BitXor(): return "^"
        case Div(): return "/"
        case FloorDiv(): return "//"
        case LShift(): return "<<"
        case RShift(): return ">>"
        case Mod(): return "%"
        case Mult(): return "*"
        case MatMult(): return "*"
        case Pow(): return "**"
        case Sub(): return "-"
        case Invert(): return "-"
        case Not(): return "!"
        case UAdd(): return "+"
        case USub(): return "-"
        case Eq(): return "="
        case Gt(): return ">"
        case GtE(): return ">="
        case Lt(): return "<"
        case LtE(): return "<="
        case NotEq(): return "!="
        case NotIn(): return "not in"
        case _: raise ValueError("No operand match")
# fmt: on


def expr_to_str(sub: Union[Name, Constant, BinOp]) -> str:
    if isinstance(sub, Name):
        return sub.id
    elif isinstance(sub, Constant):
        return str(sub.value)
    elif isinstance(sub, BinOp):
        return "{} {} {}".format(expr_to_str(sub.left), op_to_str(sub.op), expr_to_str(sub.right))


class Bound:
    upper: Union[int, str]
    lower: Union[int, str]
    step: Union[int, str]

    def __init__(self, args: List[AST]):
        if len(args) == 1:
            self.upper = args[0].value if isinstance(
                args[0], Constant) else args[0].id
            self.lower = 0
            self.step = 1
        elif len(args) == 2:
            self.upper = args[0].value if isinstance(
                args[0], Constant) else args[0].id
            self.lower = args[1].value if isinstance(
                args[1], Constant) else args[1].id
            self.step = 1
        elif len(args) == 2:
            self.upper = args[0].value if isinstance(
                args[0], Constant) else args[0].id
            self.lower = args[1].value if isinstance(
                args[1], Constant) else args[1].id
            self.step = args[2].value if isinstance(
                args[2], Constant) else args[2].id
        else:
            raise ValueError("TODO: non constant range bound")

    def __repr__(self) -> str:
        return "Bound{ " + "upper:{}, lower:{} step:{}".format(self.upper, self.lower, self.step) + " }"


class SubScriptIdx:
    value: Union[int, str]

    def __init__(self, sub: Union[Name, Constant, BinOp]):
        if isinstance(sub, Name):
            self.value = sub.id
        elif isinstance(sub, Constant):
            self.value = sub.value
        elif isinstance(sub, BinOp):
            self.value = expr_to_str(sub)

    def __repr__(self) -> str:
        return "SubScriptIdx{ " + "value:{}".format(self.value) + " }"


class LoopDepInfo:
    level: int
    index: str
    bound_info: Bound
    loop: For

    def __init__(self, level, index, bound_info, for_):
        self.level = level
        self.index = index
        self.bound_info = bound_info
        self.loop = for_

    def __repr__(self) -> str:
        return "LoopDepInfo{\n" + "  lvl:{},\n  idx:{},\n  bounds:{},\n".format(self.level, self.index, self.bound_info) + "}"

class Expression:
    value: Union[int, str]

    def __init__(self, sub: Union[Name, Constant, BinOp]):
        if isinstance(sub, Name):
            self.value = sub.id
        elif isinstance(sub, Constant):
            self.value = sub.value
        elif isinstance(sub, BinOp):
            self.value = expr_to_str(sub)

    def __repr__(self) -> str:
        return "Assignment{ " + "value:{}".format(self.value) + " }"


class Assignment:
    value: Expression

    def __init__(self, e: expr):
        if isinstance(sub, Name):
            self.value = sub.id
        elif isinstance(sub, Constant):
            self.value = sub.value
        elif isinstance(sub, BinOp):
            self.value = expr_to_str(sub)

    def __repr__(self) -> str:
        return "Assignment{ " + "value:{}".format(self.value) + " }"
