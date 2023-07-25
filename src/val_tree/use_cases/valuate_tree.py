#!/usr/bin/env python3
def valuate(ochrana_prirody, tree_presenter, tree):
    return tree_presenter.write_valuation(tree, ochrana_prirody.valuate_tree(tree))