import os
import sys

from oiTerminal.utils.configFolder import ConfigFolder


def main(folder: str):
    config_folder = ConfigFolder(folder).get_root_folder()
    if config_folder is None:
        os.makedirs(folder)
        print(folder + ' Created')
    else:
        print(config_folder + ' Exist', file=sys.stderr)

    print('Usage:')
    print('\tpython3 -m venv venv')
    print('\tsource venv/bin/active')
