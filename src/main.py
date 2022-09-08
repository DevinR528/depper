from argparse import ArgumentError
from ast import AST, Call, Constant, For, FunctionDef, Module, parse, dump
from sys import argv
from typing import List, Iterable, Union

from util import flatten


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
        if len(args) == 2:
            self.upper = args[0].value if isinstance(
                args[0], Constant) else args[0].id
            self.lower = args[1].value if isinstance(
                args[1], Constant) else args[1].id
            self.step = 1
        if len(args) == 2:
            self.upper = args[0].value if isinstance(
                args[0], Constant) else args[0].id
            self.lower = args[1].value if isinstance(
                args[1], Constant) else args[1].id
            self.step = args[2].value if isinstance(
                args[2], Constant) else args[2].id

    def __repr__(self) -> str:
        return "{ " + "upper:{}, lower:{} step:{}".format(self.upper, self.lower, self.step) + " }"


class LoopDepInfo:
    level: int
    index: str
    bound_info: Bound

    def __init__(self, level, index, bound_info):
        self.level = level
        self.index = index
        self.bound_info = bound_info

    def __repr__(self) -> str:
        return "{\n" + "  lvl:{},\n  idx:{},\n  bounds:{},\n".format(self.level, self.index, self.bound_info) + "}"


def peel_loop_info(stmt: For, lvl: int):
    infos = []
    if isinstance(stmt, For) and isinstance(stmt.iter, Call) and stmt.iter.func.id == 'range':
        print(dump(stmt))

        index = stmt.target.id
        bound = Bound(stmt.iter.args)
        for inner in stmt.body:
            lvl += 1
            infos.extend(flatten(peel_loop_info(inner, lvl)))
        infos.append(LoopDepInfo(lvl, index, bound))
    return infos


def main():
    if (len(argv) < 1):
        raise ArgumentError

    mod: Module
    with open(argv[1], 'r') as file:
        code = file.read()
        mod = parse(code, argv[1])

    infos = []
    for func in mod.body:
        if isinstance(func, FunctionDef):
            for stmt in func.body:
                print(dump(stmt))
                infos.extend(peel_loop_info(stmt, 0))

    print(list(reversed(infos)))


if __name__ == '__main__':
    main()
