#!/usr/bin/env python3

import collections as cl
import functools   as ft
import itertools   as it

import src.val_tree.adapters.excell as excell
import src.val_tree.libs.util as util


HABITAT_ABBR = {
    'výsledný obvod'                   : 'VO',
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
    'rozsáhlý charakter'                   : '*_R',
}

# def iter_bio_elements(microhabitats, extensive_microhabitats):
#     habitat_abbr = lambda h: HABITAT_ABBR[h]
#     return tuple(it.chain(
#             zip(map(habitat_abbr, microhabitats), it.repeat('A')),
#             zip(map(habitat_abbr, extensive_microhabitats), it.repeat('R')),
#         ))


# def bio_elements_cells(ws, r_idx, c_idx, el_it):
#     util.dorun(it.starmap(
#         lambda r, x: excell.cell(ws, r, c_idx, x),     enumerate(map(util.first,  el_it), r_idx)))
#     util.dorun(it.starmap(
#         lambda r, x: excell.cell(ws, r, c_idx + 1, x), enumerate(map(util.second, el_it), r_idx)))


HEADER_ITEMS = cl.OrderedDict({
    'ID'                    : lambda w: excell.cell(w, 1,  1, 'ID'),
    'Název'                 : lambda w: excell.cell(w, 1,  2, 'Název'),
    'Název Lat.'            : lambda w: excell.cell(w, 1,  3, 'Název Lat.'),
    'Průměr Kmene [cm]'     : lambda w: excell.cell(w, 1,  4, 'Průměr Kmene [cm]'),
    'Obvod Kmene [cm]'      : lambda w: excell.cell(w, 1,  5, 'Obvod Kmene [cm]'),
    'Výška Stromu [m]'      : lambda w: excell.cell(w, 1,  6, 'Výška Stromu [m]'),
    'Výška Koruny [m]'      : lambda w: excell.cell(w, 1,  7, 'Výška Koruny [m]'),
    'Průměr Koruny [m]'     : lambda w: excell.cell(w, 1,  8, 'Průměr Koruny [m]'),
    'Vitalita'              : lambda w: excell.cell(w, 1, 9, 'Vitalita'),
    'Zdravotní Stav'        : lambda w: excell.cell(w, 1, 10, 'Zdravotní Stav'),
    'Atraktivita'           : lambda w: excell.cell(w, 1, 11, 'Atraktivita'),
    'Růstové podmínky'      : lambda w: excell.cell(w, 1, 12, 'Růstové podmínky'),
    'Nadlimitní A/N'        : lambda w: excell.cell(w, 1, 13, 'Nadlimitní ANO/NE'),
    'Hodnota [CZK]'         : lambda w: excell.cell(w, 1, 14, 'Hodnota [CZK]'),
    'Poznámky'              : lambda w: excell.cell(w, 1, 15, 'Poznámky'),
})

DATA_ITEMS = cl.OrderedDict({
    'ID'                    : lambda w, r, m, t, _: \
            excell.row_merged_cell(w, r,  1, m, t['id']),
    'Název'                 : lambda w, r, m, t, _: \
            excell.row_merged_cell(w, r,  2, m, t['name'].capitalize()),
    'Název Lat.'            : lambda w, r, m, t, _: \
            excell.row_merged_cell(w, r,  3, m, t['name_lat'].capitalize()),
    'Průměr Kmene [cm]'     : lambda w, r, m, t, _: \
            excell.row_merged_cell(w, r,  4, m, ';'.join(map(str, t['diameters_cm']))),
    'Obvod Kmene [cm]'      : lambda w, r, m, t, _: \
            excell.row_merged_cell(w, r,  5, m, ';'.join(map(str, t['radiuses_cm'] or []))),
    'Výška Stromu [m]'      : lambda w, r, m, t, _: \
            excell.row_merged_cell(w, r,  6, m, t['height_m']),
    'Výška Koruny [m]'      : lambda w, r, m, t, _: \
            excell.row_merged_cell(w, r,  7, m, t['stem_height_m']),
    'Průměr Koruny [m]'     : lambda w, r, m, t, _: \
            excell.row_merged_cell(w, r,  8, m, t['crown_diameter_m']),
    'Vitalita'              : lambda w, r, m, t, _: \
            excell.row_merged_cell(w, r, 9, m, t['vitality']),
    'Zdravotní Stav'        : lambda w, r, m, t, _: \
            excell.row_merged_cell(w, r, 10, m, t['health']),
    'Atraktivita'           : lambda w, r, m, t, _: \
            excell.row_merged_cell(w, r, 11, m, t['location_attractiveness']),
    'Růstové podmínky'           : lambda w, r, m, t, _: \
            excell.row_merged_cell(w, r, 12, m, t['growth_conditions']),
    'Nadlimitní ANO/NE'     : lambda w, r, m, t, _: \
            excell.row_merged_cell(w, r, 13, m, 'A' if t['overlimit'] else 'N'),
    'Hodnota [CZK]'         : lambda w, r, m, _, v: \
            excell.cell_comma_sep(excell.row_merged_cell(w, r, 14, m, v['value_czk'])) \
                if isinstance(v['value_czk'],int) else \
                        excell.cell_red_color(excell.cell_comma_sep(excell.row_merged_cell(w, r, 14, m, v['value_czk'])))
                    ,
    'Poznámky'              : lambda w, r, m, t, _: \
            excell.row_merged_cell(w, r, 15, m, t['notes']),
})

def append_valuation(ws, r_idx, tree, value):
    n_merged = max(1, len(tree['microhabitats']) + len(tree['extensive_microhabitats']))
    n_merged = 1
    util.dorun(map(lambda f: f(ws, r_idx, n_merged, tree, value), DATA_ITEMS.values()))
    return r_idx + n_merged


class TreePresenter:
    def __init__(self, workbook):
        self.workbook   = workbook
        self.tree_sheet = workbook.open_sheet('oceneni_stromy')
        self.write_header(self.tree_sheet, HEADER_ITEMS)

        self.r_idx            = 2
        self.name_max_len     = 0
        self.lat_name_max_len = 0

    def write_header(self, ws, header_items):
        ws.delete_rows(1)
        ws.insert_rows(1)
        cell_it  = tuple(map(lambda f: f(ws), header_items.values()))
        util.dorun(map(ft.partial(excell.cell_font, {
            'name' : 'FreeMono',
            'bold' : True,
            'size' : 8}), cell_it))
        util.dorun(map(ft.partial(excell.cell_alignment, {
            'horizontal'   : 'center',
            'vertical'     : 'center',
            'textRotation' : 90}), util.drop(1, cell_it)))
        util.dorun(map(ft.partial(excell.cell_alignment, {
            'horizontal' : 'center',
            'vertical'   : 'center'}), util.take(1, cell_it)))
        util.dorun(map(ft.partial(excell.cell_color,{
                'color':'C0C0C0'}), cell_it))
        excell.fit_row_height(ws, 1, max(map(len, header_items.keys())))
        #copilot, please color header row to light gray
        
        

    def write_valuation(self, tree, value):
        self.r_idx            = append_valuation(self.tree_sheet, self.r_idx, tree, value)
        self.name_max_len     = max(self.name_max_len,     len(tree['name']))
        self.lat_name_max_len = max(self.lat_name_max_len, len(tree['name_lat']))
        excell.fit_col_width(self.tree_sheet, 2, self.name_max_len)
        excell.fit_col_width(self.tree_sheet, 3, self.lat_name_max_len)
        return (tree, value)

    def write_footer(self):
        data_it   = it.starmap(lambda k, v: (v, k), HABITAT_ABBR.items())
        write_row = util.compose(util.dorun, ft.partial(excell.iter_cell_row, self.tree_sheet))
        util.dorun(it.starmap(write_row, enumerate(data_it, self.r_idx + 2)))


def make(workbook):
    return TreePresenter(workbook)

