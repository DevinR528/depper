from argparse import ArgumentError

# fmt: off
from ast import (
    AnnAssign, Assign, AugAssign, BinOp, Call, Constant,
    For, FunctionDef, Module, Name, Subscript,
    expr, parse, dump,
)
# fmt: on
from sys import argv
from typing import List

from util import flatten, TODO
from loop_info import LoopDepInfo, Bound, SubScriptIdx
from expr_info import Assignment, Expression


def walk_stmts_collect_info(stmt: For, lvl: int) -> List[LoopDepInfo]:
    loop_infos = []
    var_infos = []
    # This is our fortran DO loop, the only thing we detect is `for var in range(...)`
    if (
        isinstance(stmt, For)
        and isinstance(stmt.iter, Call)
        and stmt.iter.func.id == 'range'
    ):
        index = stmt.target.id
        bound = Bound(stmt.iter.args)
        for inner in stmt.body:
            lvl += 1
            loop_infos.extend(flatten(walk_stmts_collect_info(inner, lvl)))
            lvl -= 1
        loop_infos.append(LoopDepInfo(lvl, index, bound, stmt))

    # Any assignment that contains a subscript (array index), we are pretending nothing else exists
    # i.e. `dictionary['crap']`
    elif isinstance(stmt, (Assign, AugAssign, AnnAssign)):
        for t in stmt.targets:
            var_infos.append(Expression(t))
        ass: Assignment
        if len(var_infos) == 1:
            ass = Assignment(left=var_infos[0], right=Expression(stmt.value), lvl=lvl)
        else: raise TODO('make destructure assignment work...')
        print("vars:\n", ass, "\n")

    else: raise TODO('more stmt types')

    return loop_infos


ERR_MSG = "must specify a python file\nusage: depper <path/to/file.py>"


def main():
    if len(argv) < 2:
        raise ArgumentError(None, message=ERR_MSG)

    mod: Module
    with open(argv[1], 'r') as file:
        code = file.read()
        mod = parse(code, argv[1])

    loop_infos = []
    for func in mod.body:
        # TODO:
        # This only handles toplevel functions, not globals
        # or other toplevel statements kinds
        if isinstance(func, FunctionDef):
            for stmt in func.body:

                # print(dump(stmt), "\n")

                loop_infos.extend(walk_stmts_collect_info(stmt, 0))

    print(list(reversed(loop_infos)))


if __name__ == '__main__':
    main()
