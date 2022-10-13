# fmt: off
from ast import (
    AST, BinOp, Constant, For, Name
)
# fmt: on
from typing import List, Union
# from typing_extensions import Self

from expr_info import expr_to_str, Expression
from typing_extensions import Self

class Bound:
    upper: Expression
    lower: Expression
    step: Expression

    def __init__(self, args: List[AST]) -> Self:
        if len(args) == 1:
            self.upper = args[0].value if isinstance(args[0], Constant) else args[0].id
            self.lower = 0
            self.step = 1
        elif len(args) == 2:
            self.upper = args[0].value if isinstance(args[0], Constant) else args[0].id
            self.lower = args[1].value if isinstance(args[1], Constant) else args[1].id
            self.step = 1
        elif len(args) == 2:
            self.upper = args[0].value if isinstance(args[0], Constant) else args[0].id
            self.lower = args[1].value if isinstance(args[1], Constant) else args[1].id
            self.step = args[2].value if isinstance(args[2], Constant) else args[2].id
        else:
            raise ValueError("TODO: non constant range bound")

    def __repr__(self) -> str:
        return (
            "Bound{ "
            + "upper:{}, lower:{} step:{}".format(self.upper, self.lower, self.step)
            + " }"
        )


class SubScriptIdx:
    value: Union[int, str]

    def __init__(self, sub: Union[Name, Constant, BinOp]) -> Self:
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

    def __init__(self, level, index, bound_info, for_) -> Self:
        self.level = level
        self.index = index
        self.bound_info = bound_info
        self.loop = for_

    def __repr__(self) -> str:
        return (
            "LoopDepInfo{\n"
            + "  lvl:{},\n  idx:{},\n  bounds:{},\n".format(
                self.level, self.index, self.bound_info
            )
            + "}"
        )
