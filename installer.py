import os
import sys
from pathlib import Path
import subprocess

if len(sys.argv) > 1:
    install_path = Path(sys.argv[1])
else:
    if 'XDG_CONFIG_HOME' in os.environ:
        install_path = Path(os.environ['XDG_CONFIG_HOME'])/'pyviewer'/'src'
    else:
        install_path = Path('~/.config/pyviewer/src').expanduser()
if install_path.exists():
    print('{} already exists.'.format(install_path))
    exit()
if not install_path.parent.exists():
    print('creating directory {}\n'.format(install_path.parent))
    os.mkdir(install_path.parent)

subprocess.run(['git', 'clone', '--recursive',
                'https://github.com/MeF0504/pyviewer.git', install_path])

if 'PATH' in os.environ \
   and str(install_path/'bin') not in os.environ['PATH'].split(os.pathsep):
    print('\nplease add {} to your PATH.'.format(install_path/'bin'))
if 'SHELL' in os.environ:
    if 'zsh' in os.environ['SHELL']:
        zsh_cmp = install_path/'shell/completion.zsh'
        print('\nplease add \'[[ -f "{}" ]] && source "{}"\' in your .zshrc.'.format(zsh_cmp, zsh_cmp))
    if 'bash' in os.environ['SHELL']:
        bash_cmp = install_path/'shell/completion.bash'
        print('\nplease add \'[[ -f "{}" ]] && source "{}"\' in your .bashrc.'.format(bash_cmp, bash_cmp))
