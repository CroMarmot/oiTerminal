# TODO
# move all const string here example all folder file name
# COLOR
import os

RED = '\e[31m'
DEFAULT = '\e[39m'
GREEN = '\e[32m'
# FOLDER
DIST = 'dist/'
TEST_FOLDER = 'TEST/'
# FILE
ROOT_PATH = os.path.dirname(os.path.realpath(__file__)) + '/'
CONFIG_FILE = ROOT_PATH + 'config.json'
STATE_FILE = 'state.json'
TEST_PY = 'test.py'
SUBMIT_PY = 'submit.py'
LANG_COFIG_FILE = ROOT_PATH + 'lang.json'

IN_SUFFIX = '.in.'
OUT_SUFFIX = '.out.'
