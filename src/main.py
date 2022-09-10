from argparse import ArgumentError
from ast import AnnAssign, Assign, AugAssign, BinOp, Call, Constant, For, FunctionDef, Index, Module, Name, Subscript, parse, dump
from sys import argv

from util import flatten
from loop_info import LoopDepInfo, Bound, SubScriptIdx


def peel_loop_info(stmt: For, lvl: int):
    loop_infos = []
    index_infos = []
    if isinstance(stmt, For) and isinstance(stmt.iter, Call) and stmt.iter.func.id == 'range':
        print(dump(stmt))

        index = stmt.target.id
        bound = Bound(stmt.iter.args)
        for inner in stmt.body:
            lvl += 1
            loop_infos.extend(flatten(peel_loop_info(inner, lvl)))
        loop_infos.append(LoopDepInfo(lvl, index, bound, stmt))
    elif isinstance(stmt, (Assign, AugAssign, AnnAssign)):
        subscript = stmt.targets[0]
        while isinstance(subscript, Subscript):
            if isinstance(subscript.slice.value, (BinOp, Name, Constant)):
                index_infos.append(SubScriptIdx(subscript.slice.value))
            if isinstance(subscript.value, Subscript):
                subscript = subscript.value
                if isinstance(subscript.value, Name):
                    index_infos.append(SubScriptIdx(subscript.slice.value))
                    print(subscript.value.id)
                    break
        print(index_infos)
    return loop_infos


def main():
    if (len(argv) < 1):
        raise ArgumentError

    mod: Module
    with open(argv[1], 'r') as file:
        code = file.read()
        mod = parse(code, argv[1])

    loop_infos = []
    for func in mod.body:
        if isinstance(func, FunctionDef):
            for stmt in func.body:
                print(dump(stmt))
                loop_infos.extend(peel_loop_info(stmt, 0))

    print(list(reversed(loop_infos)))


if __name__ == '__main__':
    main()
