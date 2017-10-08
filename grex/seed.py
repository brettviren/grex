#!/usr/bin/env python
'''
Discover DAQ runs
'''

import grex.commands

canonical_glob = "/dsk/?/data/oper/*/*/*T*"


def by_host(host, pattern=canonical_glob):
    '''
    Return seeds from given host
    '''
    cfg = dict(host=host, command="ls -d %s"%canonical_glob)
    dirs = grex.commands.remote(cfg).split('\n')
    ret = list()
    for datadir in dirs:
        datadir = datadir.strip()
        if not datadir:
            continue
        #print (datadir)
        subdirs = datadir.split('/')
        cat,cfg,ts = subdirs[-3:]
        ret.append(dict(host=host,category=cat,config=cfg,timestamp=ts,datadir=datadir))
    return ret

