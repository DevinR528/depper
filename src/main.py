from argparse import ArgumentError

# fmt: off
from ast import (
    AnnAssign, Assign, AugAssign, BinOp, Call, Constant,
    For, FunctionDef, Module, Name, Subscript,
    expr, parse, dump,
)
# fmt: on
from sys import argv

from util import flatten
from loop_info import Assignment, Expression, LoopDepInfo, Bound, SubScriptIdx


def make_expression(e: expr) -> Expression:
    index_infos = []
    is_array_ref = False
    target = e
    while isinstance(target, Subscript):
        is_array_ref = True
        # Pull out the indexing value
        if isinstance(target.slice, (BinOp, Name, Constant)):
            index_infos.append(SubScriptIdx(target.slice))
        # Python represents the subscripts nested like `[[array_name, indexed_by], indexed_by]`
        # with the innermost Subscript having the array name
        #
        # We just got the `indexed_by` value now we need to check for the array name
        if isinstance(target.value, Subscript):
            target = target.value
            # We reached the inner most index and can pull out the array name
            if isinstance(target.value, Name):
                index_infos.append(SubScriptIdx(target.slice))
                return Expression((target.value.id, list(reversed(index_infos))))

    # If we have not already saved this assignment we need to track it
    if not is_array_ref:
        return Expression(target)

    return None


def peel_loop_info(stmt: For, lvl: int):
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
            loop_infos.extend(flatten(peel_loop_info(inner, lvl)))
            lvl -= 1

        loop_infos.append(LoopDepInfo(lvl, index, bound, stmt))

    # Any assignment that contains a subscript (array index), we are pretending nothing else exists
    # i.e. `hashmap['crap']`
    elif isinstance(stmt, (Assign, AugAssign, AnnAssign)):
        # TODO:
        # This only deals with the left hand side of any assignment. Have an Assignment class
        # that has all expressions with the ability to later relate array indexing with the
        # array definition and named indexing with the definition of that name...
        for t in stmt.targets:
            var_infos.append(make_expression(t))

        ass: Assignment
        if len(var_infos) == 1:
            print("VALUE: ", dump(stmt.value))
            ass = Assignment(
                left=var_infos[0], right=make_expression(stmt.value), lvl=lvl
            )

        print("vars:\n", ass, "\n")

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
        if isinstance(func, FunctionDef):
            for stmt in func.body:
                print(dump(stmt))
                loop_infos.extend(peel_loop_info(stmt, 0))

    print(list(reversed(loop_infos)))


if __name__ == '__main__':
    main()
