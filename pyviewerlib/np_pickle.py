import os
from pathlib import PurePath
from functools import partial

import numpy as np
from numpy.lib.npyio import NpzFile

from . import args_chk, print_key, set_numpy_format, debug_print, json_opts,\
    interactive_view, interactive_cui
from .numpy import show_numpy
from .pickle import show_func as show_pickle, get_contents as get_pickle
set_numpy_format(np)


def show_func(data, path, **kwargs):
    res = ''
    err = None
    parts = PurePath(path).parts
    if len(parts) < 1:
        return '', ' something wrong, path is too short.'
    if len(parts) == 1:
        res = '{}'.format(data[parts[0]])
    else:
        pdata = data[parts[0]]
        assert pdata.dtype == np.dtype('O')
        res, err = show_pickle(pdata.item(), os.sep.join(parts[1:]))
    return res, err


def get_contents(data, path):
    dirs = []
    files = []
    parts = PurePath(path).parts
    if len(parts) == 0:
        for k in data.keys():
            if data[k].dtype == np.dtype('O'):
                dirs.append(k)
            else:
                files.append(k)
    else:
        pdata = data[parts[0]]
        assert pdata.dtype == np.dtype('O')
        dirs, files = get_pickle(pdata.item(), os.sep.join(parts[1:]))
    return dirs, files


def show_data(data, key):
    print_key(key)
    if data[key].dtype == np.dtype('O'):
        # object
        print(data[key].item())
    else:
        print(data[key])
        show_numpy(data[key])


def main(fpath, args):
    if args_chk(args, 'encoding'):
        debug_print('set encoding from args')
        encoding = args.encoding
    else:
        encoding = json_opts['pickle_encoding']
    debug_print('encoding: {}'.format(encoding))

    data = np.load(fpath, allow_pickle=True, encoding=encoding)
    if type(data) != NpzFile:
        print('please use --type numpy')
        return
    fname = os.path.basename(fpath)
    gc = partial(get_contents, data)
    sf = partial(show_func, data)

    if args_chk(args, 'verbose'):
        for k in data.keys():
            show_data(data, k)
    elif args_chk(args, 'key'):
        if args.key:
            for k in args.key:
                show_data(data, k)
        else:
            for k in data.keys():
                print(k)
        pass
    elif args_chk(args, 'interactive'):
        interactive_view(fname, gc, sf)
    elif args_chk(args, 'cui'):
        interactive_cui(fname, gc, sf)
    else:
        for k in data.keys():
            print_key(k)
            show_numpy(data[k])
