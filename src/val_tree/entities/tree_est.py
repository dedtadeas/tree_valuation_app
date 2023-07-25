#!/usr/bin/env python3

import src.val_tree.libs.util as util


IS_ZERO_POS       = lambda x: isinstance(x, (int, float)) and 0 <= x
VALUATION_CHECKER = util.make_checker({
    'value_in_czk': util.make_validator(f'"value_in_czk" must be zero-positive', IS_ZERO_POS),
})

def from_response(resp):
    err = VALUATION_CHECKER(resp)
    if err:
        return {'value_czk': f'Failed to parse response ({", ".join(err)})'}
        #raise ValueError(f'Failed to parse response ({", ".join(err)})')
    return {'value_czk': resp['value_in_czk']}

