#!/usr/bin/env python3

import functools as ft
import math
import random
from statistics import mean
import src.val_tree.libs.util as util


def optional_apply(f, x):
    return x if None == x else f(x)


def iter_int_csv(x):
    try:   
        return tuple(map(int, filter(util.identity, str(x).replace(',', ';').split(';'))))
    except:
        return ()


HABITAT_KEYS = [
    'dutinky (A)'                      ,
    'dutiny (A)'                        ,
    'hmyzí galerie a otvory (A)'       ,
    'kmenové dutiny (A/R)'              ,
    'odlupující/odchylující se borka (A)',
    'pahýly po větvích (A)'           ,
    'plodnice hub (A)'                  ,
    'poškození borky (A)'               ,
    'rozštípnuté dřevo a trhliny (A/R)' ,
    'suché větve (A)'                ,
    'trhliny (A)'                     ,
    'vodní kapsy (A)'                 ,
    'výtok mízy (A)'                  ,
    'zduřelé, členité kořenové náběhy (A)',
]

def iter_habitats(keys_it, tags_it, m):
    h_it = zip(keys_it, util.pluck(keys_it, m) or [])
    return map(util.first, filter(lambda x: util.second(x) in tags_it, h_it))


iter_microhabitats     = ft.partial(iter_habitats, HABITAT_KEYS, ['a', 'A'])
iter_ext_microhabitats = ft.partial(iter_habitats, HABITAT_KEYS, ['r', 'R'])

def iter_names(names):
    return map(lambda s: s.strip(), names.split(r'|'))

# function that computes circumference from diameter
# use correction for diameter 25 to circumference 80
def compute_circumference(diameter):
    if diameter == 25:
        return 80
    else:
        return round(diameter * math.pi) + random.randint(1, 4)
    
# function that takes diameters or circumferences and computes the other one in integer format
# for circumference computation use compute_circumference() function
# function returns diameters, circumferences and error
# if diameters and circumferences are both present, return them
def complement_dia_circ(dtext, ctext):
    diameters = iter_int_csv(dtext)
    circs = iter_int_csv(ctext)
    err = ()
    if diameters and circs:
        return diameters, circs, err
    elif diameters:
        circs = tuple(map(compute_circumference, diameters))
        return diameters, circs, err
    elif circs:
        diameters = tuple(map(lambda c: round(c / math.pi), circs))
        return diameters, circs, err
    else:
        err = ('chybí obvod i průměr',)
        return diameters, circs, err

# function that takes using formula sqrt(dmax^2 + mean(drest)^2) 
# where dmax is the maximum diameter and drest are the rest of diameters
# and returns normalized diameters and radiuses
def normalize(t):
    dmax = max(t)
    drest = tuple(filter(lambda d: d != dmax, t))
    return round(math.sqrt(dmax**2 + mean(drest)**2))
    
# fucntion that 
# first complement diameters and radiuses 
# if there is more values fill notes with text starting with "mnohokmen (výsledný obvod: $normalized radius$)"
# returns diameters, radiuses, normalized_radius, notes and error
def get_dia_rad(dtext, ctext):
    diameters, circs, err = complement_dia_circ(dtext, ctext)
    ncircs = circs[0] if circs else None
    if len(circs) > 1:
        ncircs = normalize(circs)
        notes = f'VO: {str(ncircs)}'
    else:
        notes = ''
    return diameters, circs, ncircs, notes, err


HABITAT_ABBR = {
    'dutinky (A)'                       : 'DTK',
    'dutiny (A)'                        : 'DTN',
    'hmyzí galerie a otvory (A)'        : 'HGO',
    'kmenové dutiny (A/R)'              : 'KDN',
    'odlupující/odchylující se borka (A)': 'ODB',
    'pahýly po větvích (A)'             : 'PPV',
    'plodnice hub (A)'                  : 'PHU',
    'poškození borky (A)'               : 'POB',
    'rozštípnuté dřevo a trhliny (A/R)' : 'RDT',
    'suché větve (A)'                 :  'SVT',
    'trhliny (A)'                     : 'TRH',
    'vodní kapsy (A)'                 : 'VKA',
    'výtok mízy (A)'                    : 'VYM',
    'zduřelé, členité kořenové náběhy (A)' : 'ZCN',
}

# fuction that returns string with other notes
# if microhabitats are present then 'habitaty $iter_microhabitats(m)$, $iter_ext_microhabitats(m)$'
# if Památný strom is True then "PAMÁTNÝ STROM,"
def get_other_notes(m):
    notes = ''
    ts = tuple(iter_microhabitats(m)) + tuple(iter_ext_microhabitats(m))
    if ts:
        notes += f', habitaty[ {", ".join(map(lambda h: HABITAT_ABBR[h], tuple(iter_microhabitats(m))))}'
        notes += f', {", ".join(map(lambda h: HABITAT_ABBR[h]+"_R", tuple(iter_ext_microhabitats(m))))}]'
    if m['Památný strom (A)']:
        notes += ', PAMÁTNÝ STROM'
    if i := m['odstraněná část koruny [%]']:
        notes += f', odstraněná koruna {str(i)}%'
    return notes
    

def from_tree_dat(treedat):
    m = treedat['data']
    err = treedat['err']
    # Get limit tree (Ano/Ne)
    cz, lat = iter_names(m['Český název | Latinský název'])
    diameters, radiuses, nradius, rdnotes, rderr  = get_dia_rad(m['průměr kmene [cm]'], m['obvod kmene [cm]'])
    notes = ", ".join(filter(None,[m['Poznámky'],rdnotes, get_other_notes(m)]))

    return {
        'id'                       : m['ID'],
        'name'                     : cz,
        'name_lat'                 : lat,
        'diameters_cm'             : diameters,
        'radiuses_cm'              : radiuses,
        'height_m'                 : optional_apply(float, m['výška stromu [m]']),
        'stem_height_m'            : optional_apply(float, m['výška nasazení koruny [m]']),
        'vitality'                 : optional_apply(int, m['vitalita']),
        'health'                   : optional_apply(int, m['zdravotní stav']),
        'crown_diameter_m'         : optional_apply(float, m['průměr koruny [m]']),
        'removed_crown_volume_perc': optional_apply(int, m['odstraněná část koruny [%]']),
        'location_attractiveness'  : optional_apply(int, m['atraktivita umístění']),
        'growth_conditions'        : optional_apply(int, m['růstové podmínky']),
        'microhabitats'            : tuple(iter_microhabitats(m)),
        'extensive_microhabitats'  : tuple(iter_ext_microhabitats(m)),
        'memorial_tree'            : bool(m['Památný strom (A)']),
        'notes'                    : notes,
        'err'                      : err + rderr,
        'normalized_radius_cm'     : nradius,
        'overlimit'                : nradius >= 80 if nradius else False,
    }

