# test help messages.
import sys
import argparse
import warnings
from pathlib import Path
from types import FunctionType

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from viewers.core import load_lib


@pytest.mark.parametrize(('filetype'), [
    ('hdf5'),
    ('pickle'),
    ('sqlite3'),
    ('np_pickle'),
    ('tar'),
    ('zip'),
    ('jupyter'),
    ('numpy'),
    ('raw_image'),
    ('xpm'),
    ])
def test_help_message(filetype):
    parser = argparse.ArgumentParser()
    args = parser.parse_args([])
    args.file = 'help'
    args.type = filetype
    lib = load_lib(args)
    assert lib is not None, 'failed to load library.'
    if hasattr(lib, 'show_help') and type(lib.show_help) is FunctionType:
        lib.show_help()
    else:
        warnings.warn(f'{filetype} does not support showing help.')
