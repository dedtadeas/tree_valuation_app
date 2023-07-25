#!/usr/bin/env python3

import functools as ft
import datetime  as dt
from time import time

import src.val_tree.libs.util as util


LINE_WIDTH = 80
CURR_DATE  = ft.partial(dt.datetime.now, dt.timezone.utc)
DATE_FMT   = '%Y%m%dT%H%M%S'

def fmt_msg(s, f_date=CURR_DATE):
    return f'[INFO][{f_date().strftime(DATE_FMT)} UTC] {s}'


def fmt_err(s, f_date=CURR_DATE):
    return f'[ERROR][{f_date().strftime(DATE_FMT)} UTC] {s}'


def fmt_fraction(n, d):
    d_len = len(str(d))
    return f'{n:>{d_len}}/{d}'


def fmt_bar(b_width, total, curr):
    curr = min(curr, total)
    fill = '#'*round(curr/total*b_width)
    return f'[{fill:<{b_width}}] {fmt_fraction(curr, total)}'


def make_prog_bar(b_width, total, l_width=LINE_WIDTH):
    bar = ft.partial(fmt_bar, b_width, total)
    return lambda curr, speed: f'{bar(curr)} ({speed:.02f} rec/s)'.center(l_width)


def make_rec_sec(f_time=time):
    start = f_time()
    def rec_sec(n_rec, f_time=time):
        nonlocal start
        end   = f_time()
        elaps = max(1e-6, end - start)
        start = start + elaps
        return n_rec/elaps
    return rec_sec


def make_avg_rec_sec():
    rec_sec = make_rec_sec()
    run_avg = util.make_ravg()
    return lambda n: run_avg(rec_sec(n))


def fmt_tree_err(row_i, err_it):
    err_msg = '\n'.join(map(lambda s: f'  - {s}', err_it))
    return f'Tree on row {row_i}:\n{err_msg}'


