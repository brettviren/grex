#!/usr/bin/env python3
'''
Task graph.
'''
import grex.commands
import grex.io

def make_node(func=None, inputs=(), params=None, value=None, **kwds):
    ret = list()
    if value:
        return value

    if func:
        func = getattr(grex.commands, func)
        ret.append(func)
        ret.append([tuple(inputs), list(inputs)])
        params = params or dict();
        params.update(**kwds)
        ret.append(params)
        return tuple(ret)
    return 
    

def loadf(graphfile, store=None):
    graw = grex.io.loadf(graphfile)
    g = dict()
    for name, dat in graw.items():
        if store:
            dat.setdefault('store', store)
        g[name] = make_node(**dat)
    return g

def make_task_graph(daqrun, **cfg):
    g = dict(
        daqrun = daqrun,
        rsync = (commands.rsync, 'daqrun', cfg.get('rsync',dict())),
#        fts = (commands.tarball, 'daqrun', 'rsync', cfg.get('fts',dict())),
#        box = (commands.bnlbox, 'daqrun', 'rsync', cfg.get('bnlbox', dict())),
#        final = ['fts','box']   # special exit node to triggers all
    )
    return g

def execute(g):
    '''
    Execute a graph
    '''
    print (g)


from dask.multiprocessing import get


    
