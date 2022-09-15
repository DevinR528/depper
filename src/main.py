from argparse import Action, ArgumentError
from ast import (
    AnnAssign, Assign, AugAssign, BinOp, Call, Constant, For,
    FunctionDef, Index, Module, Name, Subscript, parse, dump
)
from sys import argv

from util import flatten
from loop_info import Expression, LoopDepInfo, Bound, SubScriptIdx


def peel_loop_info(stmt: For, lvl: int):
    # print(dump(stmt))

    loop_infos = []
    index_infos = []
    var_infos = []
    # This is our fortran DO loop, the only thing we detect is `for var in range(...)`
    if isinstance(stmt, For) and isinstance(stmt.iter, Call) and stmt.iter.func.id == 'range':
        index = stmt.target.id
        bound = Bound(stmt.iter.args)
        for inner in stmt.body:
            lvl += 1
            loop_infos.extend(flatten(peel_loop_info(inner, lvl)))
        loop_infos.append(LoopDepInfo(lvl, index, bound, stmt))

    # Any assignment that contains a subscript (array index), we are pretending nothing else exists
    # i.e. `hashmap['crap']`
    elif isinstance(stmt, (Assign, AugAssign, AnnAssign)):
        # TODO:
        # This only deals with the left hand side of any assignment. Have an Assignment class
        # that has all expressions with the ability to later relate array indexing with the
        # array definition and named indexing with the definition of that name...
        is_array_ref = False
        subscript = stmt.targets[0]
        while isinstance(subscript, Subscript):
            is_array_ref = True
            # Pull out the indexing value
            if isinstance(subscript.slice, (BinOp, Name, Constant)):
                index_infos.append(SubScriptIdx(subscript.slice))
            # Python represents the subscripts nested like `[[array_name, indexed_by], indexed_by]`
            # with the innermost Subscript having the array name
            #
            # We just got the `indexed_by` value now we need to check for the array name
            if isinstance(subscript.value, Subscript):
                subscript = subscript.value
                # We reached the inner most index and can pull out the array name
                if isinstance(subscript.value, Name):
                    index_infos.append(SubScriptIdx(subscript.slice))
                    break
        # If we have not already saved this assignment we need to track it
        if not is_array_ref:
            var_infos.append(Expression(stmt.targets[0]))

        print(index_infos)
        print(var_infos)

    return loop_infos

ERR_MSG = "must specify a python file\nusage: depper <path/to/file.py>"
def main():
    if (len(argv) < 2):
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
