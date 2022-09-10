from ast import (
    AST, BinOp, Constant, For, Name, operator, Add, BitAnd, BitOr,
    BitXor, Div, FloorDiv, LShift, RShift, Mod, Mult, MatMult, Pow,
    Sub, Invert, Not, UAdd, USub, Eq, Gt, GtE, Lt, LtE, NotEq, NotIn
)
from typing import List, Union

# fmt: off
def op_to_str(op: operator) -> str:
    if isinstance(op, Add): return "+"
    elif isinstance(op, BitAnd): return "&"
    elif isinstance(op, BitOr): return "|"
    elif isinstance(op, BitXor): return "^"
    elif isinstance(op, Div): return "/"
    elif isinstance(op, FloorDiv): return "//"
    elif isinstance(op, LShift): return "<<"
    elif isinstance(op, RShift): return ">>"
    elif isinstance(op, Mod): return "%"
    elif isinstance(op, Mult): return "*"
    elif isinstance(op, MatMult): return "*"
    elif isinstance(op, Pow): return "**"
    elif isinstance(op, Sub): return "-"
    elif isinstance(op, Invert): return "-"
    elif isinstance(op, Not): return "!"
    elif isinstance(op, UAdd): return "+"
    elif isinstance(op, USub): return "-"
    elif isinstance(op, Eq): return "="
    elif isinstance(op, Gt): return ">"
    elif isinstance(op, GtE): return ">="
    elif isinstance(op, Lt): return "<"
    elif isinstance(op, LtE): return "<="
    elif isinstance(op, NotEq): return "!="
    elif isinstance(op, NotIn): return "not in"
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

    def __repr__(self) -> str:
        return "LoopDepInfo{ " + "upper:{}, lower:{} step:{}".format(self.upper, self.lower, self.step) + " }"


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
        return "Bound{\n" + "  lvl:{},\n  idx:{},\n  bounds:{},\n".format(self.level, self.index, self.bound_info) + "}"


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
