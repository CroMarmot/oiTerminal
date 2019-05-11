# TODO
# move all const string here example all folder file name
# COLOR
import os

RED = "\x1b[31m"
DEFAULT = "\x1b[39m"
GREEN = "\x1b[32m"
YELLOW = "\x1b[33m"
# FOLDER
ROOT_PATH = os.path.dirname(os.path.realpath(__file__)) + '/'
DIST = 'dist'
TEST_FOLDER = 'TEST/'
TEMPLATEFOLDER = 'template/'
# FILE
CONFIG_FILE = ROOT_PATH + 'config.json'
STATE_FILE = 'state.json'
TEST_PY = 'test.py'
SUBMIT_PY = 'submit.py'
LANG_COFIG_FILE = ROOT_PATH + 'lang.json'

IN_SUFFIX = '.in.'
OUT_SUFFIX = '.out.'

# CONFIG
FETCH_RESULT_INTERVAL = 2