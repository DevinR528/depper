from argparse import ArgumentError

# fmt: off
from ast import (
    AnnAssign, Assign, AugAssign, Call, For,
    FunctionDef, If, Module, parse, dump,
)
import json
# fmt: on
from sys import argv
from typing import List, Tuple
from dep_info import CtrlGraph, DepGraph, LoopInfo, NameMap

from util import flatten, TODO
from expr_info import Stmt, ForStmt, StmtKind


def build_dep_info(
    statements: List[Stmt],
) -> Tuple[LoopInfo, NameMap, DepGraph, CtrlGraph]:
    loops = LoopInfo()
    deps = DepGraph()
    ctrl = CtrlGraph()

    def recurse_stmts(
        stmts: List[Stmt], lvl: int, loops: LoopInfo, deps: DepGraph, ctrl: CtrlGraph
    ):
        for stmt in stmts:
            match stmt.kind:
                case StmtKind.FOR:
                    loops.add_loop(stmt.value, lvl)
                    ctrl.branch_for(stmt.value)

                    recurse_stmts(stmt.value.body, lvl + 1, loops, deps, ctrl)
                case StmtKind.IF:
                    ctrl.branch_if(stmt.value)
                case StmtKind.ASSIGN:
                    deps.add_write(stmt.value.left)
                    deps.add_read(stmt.value.right)

    recurse_stmts(statements, 0, loops, deps, ctrl)
    return loops, NameMap(), deps, ctrl


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
    else:
        stmts.append(Stmt(stmt, lvl))

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
                loop_infos.extend(walk_stmts_collect_info(stmt, 0))

    print(loop_infos)
    print(build_dep_info(loop_infos))


if __name__ == '__main__':
    main()
