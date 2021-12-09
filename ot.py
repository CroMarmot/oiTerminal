#!/usr/bin/env python3
# oi terminal
import argparse
import logging
from oiTerminal.utils.configFolder import ConfigFolder
from oiTerminal.utils.Logger import getLogger


def main(folder, logger: logging):
    parser = argparse.ArgumentParser(description='oiTerminal cli')
    parser.add_argument('ops', metavar='ops', type=str, nargs=1,
                        help='operations (init, config, problem). Example: ./ot.py init')
    parser.add_argument('args', type=str, nargs='*',
                        help='args...')

    args = parser.parse_args()
    # default config folder
    logger.debug(f"args: {args}")

    ops = args.ops
    # demo ./ot.py problem Codeforces 1613A
    if ops[0] == 'problem':
        from oiTerminal.cli import problem
        problem.main(argv=args.args, logger=logger, folder=folder)
    elif ops[0] == 'config':
        from oiTerminal.cli import config
        config.main(folder=folder, logger=logger)
    elif ops[0] == 'init':
        from oiTerminal.cli import init
        init.main(folder=folder)
    # TODO
    #   contest
    #   reg
    #   submit
    else:
        parser.print_help()


if __name__ == '__main__':
    folder = '.oiTerminal'
    config_folder = ConfigFolder(folder)
    logger = getLogger(config_folder.get_file_path('log/oiTerminal.log'))
    main(folder=folder, logger=logger)

# DEBUG
# OITERMINAL_ENV=dev
