#!/usr/bin/env python3
'''
Some GrEx command batteries included.
'''
import os
import json
import subprocess

import grex.io
import grex.store

def reformat(inputs, kwds):
    for k,v in zip(*inputs):
        kwds[k] = v;
    return kwds

def echo(inputs, params):
    params = reformat(inputs, params)

    try:
        store = params.pop("store")
    except KeyError:
        pass
    else:
        ses = grex.store.session(store)
        got = ses.query(grex.store.Stages).filter_by(command="echo", params=params).all()
        if len(got) == 1:
            return got[0].result
        if len(got) > 1:
            raise ValueError("ECHO: got %d results: %s" % (len(got), repr(got)))
        print ("PARAMS:", params)


    string = grex.io.render_string(params["message"], **params)
    print("ECHO:",string)
    return string
    







def remote(cfg):
    userat = ""
    if 'user' in cfg:
        userat = "{user}@".format(**cfg)
    cfg.setdefault('userat',userat)

    ret = subprocess.check_output("ssh {userat}{host} {command}".format(**cfg),
                                  shell=True)
    return ret.decode()
    


def rsync(daqrun, cfg):
    unique = (("dst", cfg["dst"]))
    force = cfg.get("force", False)

    ses = store.session()

    if not force:
        past = ses.query(store.Stage).filter_by(command=='rsync',
                                                daqrun_id == daqrun.id,
                                                params == unique)
        if past:
            return past[0].results

    userat = ""
    if 'user' in cfg:
        userat = "{user}@".format(**cfg)
    cfg.setdefault('userat',userat)

    cfg.setdefault('host', daqrun.host)
    cfg.setdefault('src', daqrun.datadir)

    # "do it"
    print("rsync -av {userat}{host}:{src} {dst}".format(**cfg))
    
    result=dict(files=glob('{dst}/**'.format(**cfg)))
    s = store.Stage(daqrun=daqrun, command='rsync', params=unique, result=result)
    ses.add(s)
    ses.commit()

    return result


def tarball(src=None, dst=None, excludes=None, **params):
    '''
    Make tarball `dst` from directory `src`. 
    '''
    print ("tar -xf {dst} {src}".format(**locals()))
    
