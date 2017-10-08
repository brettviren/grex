#!/usr/bin/env python3


from dask.multiprocessing import get
#from dask import get
import json

import os
import shutil

def cp_fun(src, dst):
    ret = dict(src=src, dst=dst)
    if os.path.exists(dst):
        print ("HAVE  CP: {} {}".format(src, dst))
        return ret
    print ("DOING CP: {} {}".format(src, dst))
    shutil.copy(src, dst)
    return ret

def sel_key(dat, key):
    return dat[key]

def tar_fun(src):
    dst = src + ".tar"
    ret = dict(src=src, dst=dst)
    if os.path.exists(dst):
        print ("HAVE  TAR: {} {}".format(src, dst))
        return ret
    print ("DOING TAR: {} {}".format(src, dst))
    shutil.copy(src, dst)
    return ret

def ls_fun(ins, *args):
    ret = len(ins)
    print ("LS: got %d:" % ret)
    for count, arg in enumerate(ins):
        print("LS: \t%d %s" % (count, arg))
    return ret

def make_graph(seed, dest):
    graph = dict(
        seed = seed,
        copy = (cp_fun, 'seed', dest),
        getsrc = (sel_key, 'copy', 'src'),
        getdst = (sel_key, 'copy', 'dst'),
        tarsrc = (tar_fun, 'getsrc'),
        tardst = (tar_fun, 'getdst'),
        ls = (ls_fun, ['tarsrc','tardst'], ['a', 'b'], dict(c=32)),
        )
    return graph


ginst = make_graph('/tmp/test-dask/seed', '/tmp/test-dask/copy')
print ("Graph:")

def printkeys(key, dask, state):
    print("Computing: {0} {0}".format(repr(key), repr(state)))

from dask.callbacks import Callback
with Callback(pretask=printkeys):
    for key in "ls tardst tarsrc getdst getsrc copy seed".split():
        print ("KEY: {}\t{}".format(key, repr(get(ginst, key))))
