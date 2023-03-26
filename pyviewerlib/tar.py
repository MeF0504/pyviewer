import os
import tarfile
import tempfile
import platform
from functools import partial

from . import args_chk, print_key, cprint, debug_print, get_image_viewer,\
    is_image, interactive_view, interactive_cui, show_image_file
from pymeflib.tree2 import branch_str, TreeViewer, show_tree


def show_tar(tar_file, args, get_contents, cpath, cui=False):
    res = []
    img_viewer = get_image_viewer(args)
    # check cpath
    try:
        if cpath.endswith('/'):
            key_name = cpath[:-1]
        else:
            key_name = cpath
        if platform.system() == "Windows":
            key_name = key_name.replace('\\', '/')
        tarinfo = tar_file.getmember(key_name)
    except KeyError as e:
        debug_print(e)
        return [], 'Error!! Cannot open {}.'.format(cpath)

    # file
    if tarinfo.isfile():

        # image file
        if is_image(key_name):
            cond = cui and (img_viewer not in ['PIL', 'matplotlib', 'OpenCV'])
            with tempfile.TemporaryDirectory() as tmpdir:
                tar_file.extractall(path=tmpdir, members=[tarinfo])
                tmpfile = os.path.join(tmpdir, cpath)
                ret = show_image_file(tmpfile, args, cond)
            if not ret:
                return [], 'Failed to show image.'

        # text file?
        else:
            for line in tar_file.extractfile(key_name):
                try:
                    res.append(line.decode().replace("\n", ''))
                except UnicodeDecodeError as e:
                    return [], 'Error!! {}'.format(e)
        res.append('')

    # directory
    elif tarinfo.isdir():
        tree = TreeViewer(tar_file.name, get_contents)
        res.append('{}/'.format(key_name))
        dirs, files = tree.get_contents('', key_name)
        for f in files:
            res.append('{}{}'.format(branch_str, f))
        for d in dirs:
            res.append('{}{}/'.format(branch_str, d))
    else:
        res.append('sorry, I can\'t show information.\n')

    return res, None


def get_contents(tar_file, root, path):
    path = str(path)
    if path == '.':
        tarinfo = tar_file.getmembers()[0]
        if tarinfo.isfile():
            return [], [tarinfo.name]
        elif tarinfo.isdir():
            return [tarinfo.name], []
        else:
            return [], []
    files = []
    dirs = []
    for t in tar_file.getmembers():
        if t.name == path:
            continue
        if not t.name.startswith(path):
            continue
        tname = t.name[len(path)+1:]
        if '/' in tname:
            continue
        if t.isfile():
            files.append(tname)
        elif t.isdir():
            dirs.append(tname)
    return dirs, files


def main(fpath, args):
    if not tarfile.is_tarfile(fpath):
        print('{} is not a tar file.'.format(fpath))
        return
    tar_file = tarfile.open(fpath, 'r:*')
    fname = os.path.basename(fpath)

    if args_chk(args, 'interactive'):
        interactive_view(fname, partial(get_contents, tar_file),
                         partial(show_tar, tar_file, args,
                                 partial(get_contents, tar_file)))
    elif args_chk(args, 'cui'):
        interactive_cui(fpath, partial(get_contents, tar_file),
                        partial(show_tar, tar_file, args,
                                partial(get_contents, tar_file)))
    elif args_chk(args, 'key'):
        if len(args.key) == 0:
            tar_file.list(verbose=False)
        for k in args.key:
            print_key(k)
            info, err = show_tar(tar_file, args,
                                 partial(get_contents, tar_file), k)
            if err is None:
                print("\n".join(info))
                print()
            else:
                cprint(err, fg='r')
    elif args_chk(args, 'verbose'):
        tar_file.list(verbose=True)
    else:
        show_tree(fname, partial(get_contents, tar_file))

    tar_file.close()
