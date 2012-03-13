import os

__author__ = 'nic'

# Dev mode enabled
DEV_MODE = True

# Application Constants
HISTORY_LENGTH = 5
WELCOME_MESSAGE = "Enter LaTeX code here"

# File paths
CACHE_PATH = os.path.join('semtex_gui','cache')
RES_PATH = os.path.join('semtex_gui','res')
APP_LOGO_PATH = os.path.join(RES_PATH, 'logo.png')
STDOUT_PATH = os.path.join(CACHE_PATH, '.outp')
HISTORY_PATH = os.path.join(CACHE_PATH, '.hist')
HEADER_PATH = os.path.join(RES_PATH, '.start')
FOOTER_PATH = os.path.join(RES_PATH, '.end')
LATEX_CODE_PATH = os.path.join(CACHE_PATH, 'temp.tex')
LATEX_OUTP_PATH = os.path.join(CACHE_PATH, 'temp.dvi')
PNG_DISP_PATH = os.path.join(CACHE_PATH, 'temp.png')
PNG_CLIP_PATH = os.path.join(CACHE_PATH, 'clip.png')

# Other Constants
PNG_TRANS = 'transparent'