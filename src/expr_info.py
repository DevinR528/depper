# fmt: off
from ast import (
    AST, BinOp, Call, Constant, For, ListComp, Name, Subscript, comprehension, dump,
    expr, operator, Add, BitAnd, BitOr, BitXor, Div, FloorDiv,
    LShift, RShift, Mod, Mult, MatMult, Pow, Sub, Invert,
    Not, UAdd, USub, Eq, Gt, GtE, Lt, LtE, NotEq, NotIn,
    List as ListAst,
)
from enum import Enum
# fmt: on
from typing import Any, List, Tuple, Union
from typing_extensions import Self

from util import TODO

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


def expr_to_str(sub: Union[Name, Constant, BinOp, Call, Subscript]) -> str:
    if isinstance(sub, Name):
        return sub.id
    elif isinstance(sub, Constant):
        return str(sub.value)
    elif isinstance(sub, BinOp):
        return "{} {} {}".format(
            expr_to_str(sub.left), op_to_str(sub.op), expr_to_str(sub.right)
        )
    elif isinstance(sub, Subscript):
        name = ""
        s = []
        while isinstance(sub, Subscript):
            if isinstance(sub.value, Name):
                name = sub.value.id
                s.append(f"[{expr_to_str(sub.slice)}]")
                break
            else:
                s.append(f"[{expr_to_str(sub.slice)}]")
                sub = sub.value
        return f"{name}{''.join(reversed(s))}"
    elif isinstance(sub, Call):
        return f"{sub.func.id}(...)"


class VarName:
    name: str

    def __init__(self, name: str) -> Self:
        self.name = name

    def __repr__(self) -> str:
        return "Var { " + f"name:{self.name}" + " }"


class ConstKind(Enum):
    INT = 0
    STR = 1
    LIST = 2


class Const:
    kind: ConstKind
    val: Union[int, str, List[Self]]

    def __init__(self, val: Union[int, str, List[Self]]) -> Self:
        match val:
            case int():
                self.kind = ConstKind.INT
            case str():
                self.kind = ConstKind.STR
            case list():
                self.kind = ConstKind.LIST
        self.val = val

    def __repr__(self) -> str:
        return "Const { " + f"value:{self.val}, kind:{self.kind}" + " }"


class BinOpKind(Enum):
    ADD = 0
    BITAND = 1
    BITOR = 2
    BITXOR = 3
    DIV = 4
    FLOORDIV = 5
    LSHIFT = 6
    RSHIFT = 7
    MOD = 8
    MULT = 9
    MATMULT = 10
    POW = 11
    SUB = 12
    INVERT = 13
    NOT = 14
    UADD = 15
    USUB = 16
    EQ = 17
    GT = 18
    GTE = 19
    LT = 20
    LTE = 21
    NOTEQ = 22
    NOTIN = 23


# fmt: off

# Python does not allow you to override the construction of enums
# in the right way to parse something in the __init__ method so we
# do this HACK
def new(cls, op: operator) -> None:
    match op:
        case Add(): return BinOpKind.ADD
        case BitAnd(): return BinOpKind.BITAND
        case BitOr(): return BinOpKind.BITOR
        case BitXor(): return BinOpKind.BITXOR
        case Div(): return BinOpKind.DIV
        case FloorDiv(): return BinOpKind.FLOORDIV
        case LShift(): return BinOpKind.LSHIFT
        case RShift(): return BinOpKind.RSHIFT
        case Mod(): return BinOpKind.MOD
        case Mult(): return BinOpKind.MULT
        case MatMult(): return BinOpKind.MATMULT
        case Pow(): return BinOpKind.POW
        case Sub(): return BinOpKind.SUB
        case Invert(): return BinOpKind.INVERT
        case Not(): return BinOpKind.NOT
        case UAdd(): return BinOpKind.UADD
        case USub(): return BinOpKind.USUB
        case Eq(): return BinOpKind.EQ
        case Gt(): return BinOpKind.GT
        case GtE(): return BinOpKind.GTE
        case Lt(): return BinOpKind.LT
        case LtE(): return BinOpKind.LTE
        case NotEq(): return BinOpKind.NOTEQ
        case NotIn(): return BinOpKind.NOTIN
        case _ as x: raise ValueError(f"No operand match {x}")

# Continue the HACK from above, hard overwriting the constructor
setattr(BinOpKind, '__new__', new)


# Forward reference for BinaryOp (come on python, you are an untyped language wtf)
class Expression: pass
# fmt: on


class BinaryOp:
    kind: BinOpKind
    left: Expression
    right: Expression

    def __init__(self, val: BinOp) -> None:
        self.kind = BinOpKind(val.op)
        self.left = Expression(val.left)
        self.right = Expression(val.right)

    def __repr__(self) -> str:
        return (
            "BinOp { "
            + f"left:{self.left}, right:{self.right}, kind:{self.kind}"
            + " }"
        )

class CallExpr:
    fn_name: VarName
    args: List[Expression]

    def __init__(self, val: Call) -> Self:
        self.fn_name = VarName(val.func.id)
        self.args = list(map(Expression, val.args))


    def __repr__(self) -> str:
        return "Call { " + f"name:{self.fn_name}, args:{self.args}" + " }"


class IndexOp:
    array: VarName
    indexes: List[Expression]

    def __init__(self, val: Subscript) -> None:
        idx = []
        while isinstance(val, Subscript):
            if isinstance(val.value, Name):
                self.array = VarName(val.value.id)
                idx.append(Expression(val.slice))
                break
            else:
                idx.append(Expression(val.slice))
                val = val.value
        self.indexes = idx

    def __repr__(self) -> str:
        return (
            "IndexOp { "
            + f"array:{self.array}, indexes:{self.indexes}"
            + " }"
        )

class GeneratorExpr:
    loop_ele: Expression
    iterable: Expression
    if_filter: Any
    is_async: bool

    def __init__(self, val: List[comprehension]) -> None:
        if len(val) > 1: raise TODO('list comprehension with multiple comps')

        print(dump(val[0]))

        comp = val[0]
        self.loop_ele = Expression(comp.target)
        self.iterable = Expression(comp.iter)
        self.is_async = bool(comp.is_async)
        if len(comp.ifs) > 0: raise TODO('found if filter in list comp')

    def __repr__(self) -> str:
        return (
            "GeneratorExpr { "
            + f"loop_ele:{self.loop_ele}, iter:{self.iterable}, async:{self.is_async}"
            + " }"
        )

class ListCompExpr:
    elem: Expression
    generator: GeneratorExpr

    def __init__(self, val: ListComp) -> None:
        print(val)
        self.elem = Expression(val.elt)
        self.generator = GeneratorExpr(val.generators)

    def __repr__(self) -> str:
        return (
            "ListCompExpr { "
            + f"ele:{self.elem}, gen:{self.generator}"
            + " }"
        )


class Expression:
    value: Union[VarName, Const, BinaryOp, List[Self], IndexOp]

    def __init__(
        self,
        value: Union[Name, Constant, BinOp, Call, ListAst, ListComp, Subscript],
    ) -> None:
        if isinstance(value, Name):
            self.value = VarName(value.id)
        elif isinstance(value, Constant):
            self.value = Const(value.value)
        elif isinstance(value, BinOp):
            self.value = BinaryOp(value)
        elif isinstance(value, Call):
            self.value = CallExpr(value)
        elif isinstance(value, ListAst):
            self.value = list(map(Expression, value.elts))
        elif isinstance(value, ListComp):
            self.value = ListCompExpr(value)
        elif isinstance(value, Subscript):
            self.value = IndexOp(value)
        else:
            print(value)
            raise TypeError("invalid type", type(value), dump(value))

    def __repr__(self) -> str:
        return "Expression { " + f"value:{self.value}" + " }"


class Assignment:
    left: Expression
    right: Expression
    loop_lvl: int
    count: int

    def __init__(self, left: Expression, right: Expression, lvl: int):
        self.left = left
        self.right = right
        self.loop_lvl = lvl

    def __repr__(self) -> str:
        return (
            "Assignment { "
            + f"loop_lvl:{self.loop_lvl}, left:{self.left}, right:{self.right}"
            + " }"
        )
