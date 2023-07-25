#!/usr/bin/env python3

import collections as cl
import functools   as ft
import itertools   as it
import operator    as op
import time


def dorun(iterable):
    cl.deque(iterable, maxlen=0)


def take(n, iterable):
    return it.islice(iterable, n)


def drop(n, iterable):
    return it.islice(iterable, n, None)


def first(iterable):
    return next(iter(iterable))


def nth(n, iterable):
    return first(drop(n, iterable))


def second(iterable):
    return nth(1, iterable)


def pluck(iterable, d):
    return op.itemgetter(*iterable)(d)


def pick(iterable, d):
    def do(acc, k):
        acc[k] = d[k]
        return acc
    return ft.reduce(do, iterable, {})


def identity(x):
    return x


def complement(f):
    return lambda *args: not f(*args)


def _compose2(f, g):
    return lambda *args: f(g(*args))


def compose(*f):
    return ft.reduce(_compose2, f)


def _any_fn2(f, g):
    return lambda *args: f(*args) or g(*args)


def any_fn(*f):
    return ft.reduce(_any_fn2, f)


def throttle(f, s, f_sleep=time.sleep):
    start = 0
    def throttled_f(*args, f_time=time.time):
        nonlocal start
        elaps = f_time() - start
        start = start + max(elaps, s)
        if (elaps < s):
            f_sleep(s - elaps)
        return f(*args)
    return throttled_f


def partition_by(fp, iterable):
    i1, i2 = it.tee(iterable)
    return (filter(fp, i1), filter(complement(fp), i2))


def make_validator(s, f):
    to_str = lambda args: ', '.join(map(str, args))
    return lambda *args: (bool(f(*args)), f'{s} ({to_str(args)})')


def make_checker(validator_dt):
    def checker(dt):
        val_it = it.starmap(lambda k, f: f(dt[k]), validator_dt.items())
        return tuple(map(second, filter(complement(first), val_it)))
    return checker

def make_ravg():
    i, avg = (0, 0)
    def ravg(n):
        nonlocal i, avg
        i   = i + 1
        avg = (avg*(i - 1) + n)/i
        return avg
    return ravg

