#! /usr/bin/env python3

import os
import sys
import argparse
from pathlib import Path
from types import FunctionType
from logging import getLogger
import subprocess

from .core import GLOBAL_CONF, VERSION, \
    get_filetype, load_lib, args_chk, print_key, get_col, cprint
from .core.image_viewer import ImageViewers
from .core.helpmsg import add_args_shell_cmp
from .core.types import Args

logger = getLogger(GLOBAL_CONF.logname)


def get_args() -> Args:
    supported_type = list(GLOBAL_CONF.types.keys()).copy()
    supported_type.remove('text')
    parser = argparse.ArgumentParser(
            description="show the constitution of a file."
            f" Supported file types ... {', '.join(supported_type)}."
            " To see the detailed help of each type, "
            " type 'pyviewer help -t <type>'.",
            epilog=" PyViewer has other subcommands,"
            " 'pyviewer help -t <type>' shows detailed help,"
            " 'pyviewer update' run PyViewer update command,"
            " 'pyviewer config_list' shows the current optional configuration,"
            " 'pyviewer shell_completion --bash >> ~/.bashrc' or"
            " 'pyviewer shell_completion --zsh >> ~/.zshrc'"
            " set the completion script for bash/zsh."
            )
    parser.add_argument('file', help='input file')
    parser.add_argument('--version', '-V', action='version',
                        version=f'%(prog)s {VERSION}')
    parser.add_argument('-t', '--type', dest='type',
                        help='specify the file type.'
                        ' "pyviewer help -t TYPE"'
                        ' will show the detailed help.',
                        choices=supported_type)
    tmpargs, rems = parser.parse_known_args()
    if tmpargs.file == 'shell_completion':
        add_args_shell_cmp(parser)
    if not args_chk(tmpargs, 'type'):
        tmpargs.type = get_filetype(Path(tmpargs.file))
    lib = load_lib(tmpargs)
    if lib is not None:
        lib.add_args(parser)
    args = parser.parse_args()
    logger.debug(f'args: {args}')
    return args


def show_opts() -> None:
    for key, val in GLOBAL_CONF.opts.items():
        if type(val) is dict:
            print_key(key)
            for k2, v2 in val.items():
                print(f'  {k2}: {v2}')
        else:
            print_key(key)
            print(val)


def set_shell_comp(args: Args) -> None:
    if args_chk(args, 'bash'):
        sh_cmp_file = Path(__file__).parent/'shell-completion/completion.bash'
    elif args_chk(args, 'zsh'):
        sh_cmp_file = Path(__file__).parent/'shell-completion/completion.zsh'
    else:
        print('Please specify shell (--bash or --zsh).')
        return
    with open(sh_cmp_file, 'r') as f:
        for line in f:
            print(line, end='')


def update() -> None:
    py_cmd = None
    py_version = f'{sys.version_info.major}.{sys.version_info.minor}'
    for rel_path in [f'bin/python{py_version}',
                     f'bin/python{sys.version_info.major}',
                     'bin/python',
                     f'python{py_version}.exe',
                     f'python{sys.version_info.major}.exe',
                     'python.exe',
                     ]:
        py_path = Path(sys.base_prefix)/rel_path
        if py_path.is_file() and os.access(py_path, os.X_OK):
            py_cmd = str(py_path)
            logger.info(f'find python; {py_cmd}')
            break
    if py_cmd is None:
        fg, bg = get_col('msg_error')
        cprint('failed to find python command.', fg=fg, bg=bg)
        logger.error(f'python not found in {sys.base_prefix}')
        return
    update_cmd = [py_cmd, '-m', 'pip', 'install', '--upgrade',
                  'pyviewer @ git+https://github.com/MeF0504/pyviewer'
                  ]
    logger.debug(f'update command: {update_cmd}')
    out = subprocess.run(update_cmd, capture_output=False)
    logger.debug(f'update command results; return code {out.returncode}')


def main() -> None:
    args = get_args()

    if args.file == 'config_list':
        show_opts()
        return

    if args.file == 'shell_completion':
        set_shell_comp(args)
        return

    if args.file == 'update':
        update()
        return

    if args.file == 'help':
        if not args_chk(args, 'type'):
            print('please set --type to see the details.')
            return
        lib = load_lib(args)
        if lib is None:
            print('Library file is not found.')
        else:
            if hasattr(lib, 'show_help') and \
               type(lib.show_help) is FunctionType:
                lib.show_help()
            else:
                print("this type does not support showing help.")
        return

    fpath = Path(args.file).expanduser()
    if not fpath.exists():
        print("file doesn't exists!")
        return
    if fpath.is_dir():
        print("{} is a directory.".format(fpath))
        return

    if not args_chk(args, 'type'):
        args.type = get_filetype(fpath)

    if args.type == 'text':
        if ('LANG' in os.environ) and ('ja_JP' in os.environ['LANG']):
            print('vimでも使ってろ！')
        else:
            print("Why Don't you use vim???")
        return

    lib = load_lib(args)
    if lib is None:
        print('Library file is not found.')
    else:
        lib.main(fpath, args)
    return


def get_types():
    if len(sys.argv) < 2:
        return ""
    elif sys.argv[1] == 'type':
        supported_type = list(GLOBAL_CONF.types.keys()).copy()
        supported_type.remove('text')
        print(' '.join(supported_type))
    elif sys.argv[1] == 'image_viewer':
        print(' '.join(ImageViewers))
