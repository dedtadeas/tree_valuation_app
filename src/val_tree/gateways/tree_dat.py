#!/usr/bin/env python3

import src.val_tree.entities.tree_dat as tree_dat
import src.val_tree.entities.tree as tree
import src.val_tree.libs.util as util

def not_empty(val_it):
    return any(val_it)

def iter_trees(workbook):
    tree_ws = workbook.open_sheet('zaznam_stromy')
    row_it  = filter(not_empty, util.drop(1, tree_ws.iter_rows(values_only=True)))
    return map(tree.from_tree_dat, map(tree_dat.from_data_row, row_it))

