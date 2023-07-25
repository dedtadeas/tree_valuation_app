#!/usr/bin/env python3

import collections as cl
import re

import src.val_tree.libs.util as util


def OPTIONAL():
    return lambda x: None == x


def MATCHES(r):
    return lambda x: r.fullmatch(str(x).strip())


TREE_VALIDATOR = cl.OrderedDict({
    'ID'                                : util.make_validator(
        f'"ID" must be positive int',
        MATCHES(re.compile(r'\d+'))),

    #'S/P'                               : util.make_validator(
    #    f'"S/P" must be one of (S, P)',
    #    util.any_fn(OPTIONAL(), MATCHES(re.compile(r'S|P', re.IGNORECASE)))),

    'Český název | Latinský název'      : util.make_validator(
        f'"Český název | Latinský název" must be non-blank',
        MATCHES(re.compile(r'(\S+\s*)+?\|\s*(\S+\s*)+'))),

    'průměr kmene [cm]'                 : util.make_validator(
        f'"průměr kmene [cm]" must contain positive ints',
        util.any_fn(OPTIONAL(), MATCHES(re.compile(r'\d+([,;]\d+)*[,;]?')))),

    'obvod kmene [cm]'                  : util.make_validator(
        f'"obvod kmene [cm]" must contain positive ints',
        util.any_fn(OPTIONAL(), MATCHES(re.compile(r'\d+([,;]\d+)*[,;]?')))),

    'výška stromu [m]'                  : util.make_validator(
        f'"výška stromu [m]" must be positive number',
        util.any_fn(OPTIONAL(), MATCHES(re.compile(r'(\d*\.\d+)|(\d+\.?)')))),

    'výška nasazení koruny [m]'         : util.make_validator(
        f'"výška nasazení koruny [m]" must be positive number',
        util.any_fn(OPTIONAL(), MATCHES(re.compile(r'(\d*\.\d+)|(\d+\.?)')))),

    'průměr koruny [m]'                 : util.make_validator(
        f'"průměr koruny [m]" must be positive number',
        util.any_fn(OPTIONAL(), MATCHES(re.compile(r'(\d*\.\d+)|(\d+\.?)')))),

    'vitalita'                          : util.make_validator(
        f'"vitalita" must be in range of <1, 5>',
        util.any_fn(OPTIONAL(), MATCHES(re.compile(r'[1-5]')))),

    'zdravotní stav'                    : util.make_validator(
        f'"zdravotní stav" must be in range of <1, 5>',
        util.any_fn(OPTIONAL(), MATCHES(re.compile(r'[1-5]')))),

    'atraktivita umístění'              : util.make_validator(
        f'"atraktivita umístění" must be in range of <1, 5>',
        util.any_fn(OPTIONAL(), MATCHES(re.compile(r'[1-5]')))),

    'růstové podmínky'                  : util.make_validator(
        f'"růstové podmínky" must be in range of <1, 5>',
        util.any_fn(OPTIONAL(), MATCHES(re.compile(r'[1-5]')))),

    'Poznámky'                 : util.make_validator(
        f'Poznámky" must be string or digits, whatever',
        util.any_fn(OPTIONAL(), MATCHES(re.compile(r'.*')))),

    'odstraněná část koruny [%]'        : util.make_validator(
        f'"odstraněná část koruny [%]" must be positive int',
        util.any_fn(OPTIONAL(), MATCHES(re.compile(r'100|\d\d|\d')))),
    
    'dutinky (A)'               : util.make_validator(
        f'"dutinky (A)" must be one of (A)',
        util.any_fn(OPTIONAL(), MATCHES(re.compile(r'A', re.IGNORECASE)))),
    
    'dutiny (A)'               : util.make_validator(
        f'"dutiny (A)" must be one of (A)',
        util.any_fn(OPTIONAL(), MATCHES(re.compile(r'A', re.IGNORECASE)))),
    
    'hmyzí galerie a otvory (A)': util.make_validator(
        f'"hmyzí galerie a otvory (A)" must be one of (A)',
        util.any_fn(OPTIONAL(), MATCHES(re.compile(r'A', re.IGNORECASE)))),
    
    'kmenové dutiny (A/R)' : util.make_validator(
        f'"kmenové dutiny (A/R)" must be one of (A, R)',
        util.any_fn(OPTIONAL(), MATCHES(re.compile(r'A|R', re.IGNORECASE)))),

    'odlupující/odchylující se borka (A)': util.make_validator(
        f'"odlupující/odchylující se borka (A)" must be one of (A)',
        util.any_fn(OPTIONAL(), MATCHES(re.compile(r'A', re.IGNORECASE)))),
    
    'pahýly po větvích (A)': util.make_validator(
        f'"pahýly po větvích (A)" must be one of (A)',
        util.any_fn(OPTIONAL(), MATCHES(re.compile(r'A', re.IGNORECASE)))),
       
    'plodnice hub (A)': util.make_validator(
        f'"plodnice hub (A)" must be one of (A)',
        util.any_fn(OPTIONAL(), MATCHES(re.compile(r'A', re.IGNORECASE)))), 

    'poškození borky (A)': util.make_validator(
        f'"poškození borky (A)" must be one of (A)',
        util.any_fn(OPTIONAL(), MATCHES(re.compile(r'A', re.IGNORECASE)))), 


    'rozštípnuté dřevo a trhliny (A/R)'                      : util.make_validator(
        f'"rozštípnuté dřevo a trhliny (A/R)" must be one of (A, R)',
        util.any_fn(OPTIONAL(), MATCHES(re.compile(r'A|R', re.IGNORECASE)))),
    
    'suché větve (A)': util.make_validator(
        f'"suché větve (A)" must be one of (A)',
        util.any_fn(OPTIONAL(), MATCHES(re.compile(r'A', re.IGNORECASE)))), 
    
    'trhliny (A)'               : util.make_validator(
        f'"trhliny (A)" must be one of (A)',
        util.any_fn(OPTIONAL(), MATCHES(re.compile(r'A', re.IGNORECASE)))),
    
    'vodní kapsy (A)'                    : util.make_validator(
        f'"vodní kapsy (A)" must be one of (A)',
        util.any_fn(OPTIONAL(), MATCHES(re.compile(r'A', re.IGNORECASE)))),
        
    'výtok mízy (A)'                    : util.make_validator(
        f'"výtok mízy (A)" must be one of (A)',
        util.any_fn(OPTIONAL(), MATCHES(re.compile(r'A', re.IGNORECASE)))),

    'zduřelé, členité kořenové náběhy (A)'                  : util.make_validator(
        f'"zduřelé, členité kořenové náběhy (A)" must be one of (A)',
        util.any_fn(OPTIONAL(), MATCHES(re.compile(r'A', re.IGNORECASE)))),

    'Památný strom (A)'                 : util.make_validator(
        f'"Památný strom (A)" must be one of (A)',
        util.any_fn(OPTIONAL(), MATCHES(re.compile(r'A', re.IGNORECASE)))),
})
TREE_CHECKER = util.make_checker(TREE_VALIDATOR)

def from_data_row(row):
    k   = dict(zip(TREE_VALIDATOR.keys(), row))
    err = TREE_CHECKER(k)
    #if err:
    #    raise ValueError(f'Failed to parse measurement ({", ".join(err)})')
    return {'data':k,'err':err}

