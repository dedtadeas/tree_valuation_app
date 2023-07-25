#!/usr/bin/env python3

import argparse
import functools as ft
import os

import src.val_tree.adapters.http as http_adp
import src.val_tree.adapters.excell as excell_adp
import src.val_tree.gateways.tree_dat as tree_dat
import src.val_tree.gateways.ochranaprirody as ochranaprirody
import src.val_tree.presenters.tree_est as tree_est
import src.val_tree.use_cases.valuate_tree as valuate_tree
import src.val_tree.libs.util as util

# Class wchich represents tree validator
class TreeComputer():
    # Constructor
    def __init__(self):
        self.output_path = None
        self.error = None
        pass
        
    def parse_args(self, args_it):
        parser = argparse.ArgumentParser()
        parser.add_argument('input-sheet', help='The input Excell sheet with measurements',
                metavar='FILE')
        parser.add_argument('--reg-sec',   help='The number of valuated items per second',
                required=False, metavar="NUM", default=2)
        return vars(parser.parse_args(args_it))

    def create_output_path(self, fpath):
        path, ext = os.path.splitext(fpath)
        return f'{path}.val.xlsx'

    def valuate_tree(self, path):
        try:
            #raise Exception('TBD')
            args         = self.parse_args([path])
            input_sheet  = excell_adp.make(path)
            output_sheet = excell_adp.make(self.create_output_path(path))   
            tree_ests = tree_est.make(output_sheet)
            val_tree = ft.partial(valuate_tree.valuate,
                ochranaprirody.make(args['reg_sec'], http_adp.make()), tree_ests)
            result = tuple(map(val_tree, util.take(5, tree_dat.iter_trees(input_sheet))))
            tree_ests.write_footer()
            output_sheet.save()
            self.output_path = self.create_output_path(path)
        except Exception as e:
            self.error = str(e)
        return