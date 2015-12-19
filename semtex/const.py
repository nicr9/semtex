from os.path import join as path_join
from pkg_resources import resource_filename

__author__ = 'nic'

# Dev mode enabled
DEV_MODE = True

# Application Constants
HISTORY_LENGTH = 5
WELCOME_MESSAGE = "Enter LaTeX code here"

# File paths
CACHE_PATH = '/tmp/semtex/'
RES_PATH = resource_filename('semtex', 'res')
APP_LOGO_PATH = resource_filename('semtex', 'res/logo.png')
STDOUT_PATH = path_join(CACHE_PATH, '.outp')
HISTORY_PATH = path_join(CACHE_PATH, '.hist')
HEADER_PATH = resource_filename('semtex', 'res/header.tex')
FOOTER_PATH = resource_filename('semtex', 'res/footer.tex')
LATEX_CODE_PATH = path_join(CACHE_PATH, 'temp.tex')
LATEX_OUTP_PATH = path_join(CACHE_PATH, 'temp.dvi')
PNG_DISP_PATH = path_join(CACHE_PATH, 'temp.png')
PNG_CLIP_PATH = path_join(CACHE_PATH, 'clip.png')

# Other Constants
PNG_TRANS = 'transparent'
