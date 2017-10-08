#!/usr/bin/env python3
'''
Task graph.
'''
import commands


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
