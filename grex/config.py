#!/usr/bin/env python3
'''
Interface to configuration files
'''

def loads(text, **params):
    '''
    Load Jsonnet text with possible extra params and return data structure.
    '''
    import json
    import _jsonnet
    jtext = _jsonnet.evaluate_snippet("grex", text, ext_vars=params)
    return json.loads(jtext)

