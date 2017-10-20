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

def by_id(ses, ids):

    seed_objs = list()
    for sid in ids:
        try:
            sid = int(sid)
            obj = ses.query(grex.store.DaqRun).filter_by(id=sid).all()
        except ValueError:
            h,cat,cfg,ts = sid.split('-')
            obj = ses.query(grex.store.DaqRun).filter_by(host=h,category=cat,config=cfg,timestamp=ts).all()
        if not obj:
            click.echo("no such seed: %s" % repr(sid))
            continue
        if len(obj) > 1:
            print("got multiple seeds for %s, using first" % repr(sid))
        seed_objs.append(obj[0])
    return seed_objs
