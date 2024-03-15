from logging import getLogger

from pymeflib.color import FG, BG, FG256, BG256, END
# values
from .core import get_config, GLOBAL_CONF
# functions
from .core import args_chk, cprint, print_key, get_col, \
    set_numpy_format, interactive_view, run_system_cmd, show_opts
# class
from .core import ReturnMessage
from .core.image_viewer import get_image_viewer, is_image, \
    show_image_file, show_image_ndarray, ImageViewers
from .core.helpmsg import help_template, \
    add_args_imageviewer, add_args_encoding, add_args_output, \
    add_args_verbose, add_args_key, add_args_interactive, add_args_cui, \
    add_args_specification
logger = getLogger(GLOBAL_CONF.logname)

try:
    from .core.cui import interactive_cui
except ImportError as e:
    logger.error(e)

    def interactive_cui(*args, **kwargs):
        print('failed to import the interactive_cui function.')
        print('maybe the curses module is not available.')
        return
