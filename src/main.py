from argparse import ArgumentError

# fmt: off
from ast import (
    AnnAssign, Assign, AugAssign, Call, For,
    FunctionDef, If, Module, parse, dump,
)
# fmt: on
from sys import argv
from typing import List

from util import flatten, TODO
from expr_info import Stmt, ForStmt


def walk_stmts_collect_info(stmt: For, lvl: int) -> List[Stmt]:
    stmts = []
    # This is our fortran DO loop, the only thing we detect is `for var in range(...)`
    if (
        isinstance(stmt, For)
        and isinstance(stmt.iter, Call)
        and stmt.iter.func.id == 'range'
    ):
        stmts.append(Stmt(stmt, lvl))

    # Any assignment that contains a subscript (array index), we are pretending nothing else exists
    # i.e. `dictionary['crap']`
    elif isinstance(stmt, (Assign, AugAssign, AnnAssign)):

        stmts.append(Stmt(stmt, lvl))
    elif isinstance(stmt, If):
         stmts.append(Stmt(stmt, lvl))
    else: raise TODO(f"more stmt types {dump(stmt)}")

    return stmts


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

    print(loop_infos)


if __name__ == '__main__':
    main()
