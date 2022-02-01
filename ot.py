#!/usr/bin/env python3
# oi terminal
import argparse
import logging
from oiTerminal.cli.constant import OT_FOLDER, OT_LOG
from oiTerminal.utils.configFolder import ConfigFolder
from oiTerminal.utils.Logger import getLogger


def main():
  folder = OT_FOLDER
  config_folder = ConfigFolder(folder)
  parser = argparse.ArgumentParser(description='oiTerminal cli')
  parser.add_argument('ops', metavar='ops', type=str, nargs=1,
                      help='operations (init, config, problem, contest, contestdetail, standing). Example: ./ot.py init')
  parser.add_argument('args', type=str, nargs='*',
                      help='args...')
  args = parser.parse_args()
  # default config folder
  logging.debug(f"args: {args}")

  ops = args.ops
  # demo ./ot.py problem Codeforces 1613A
  if ops[0] == 'init':
    from oiTerminal.cli import init
    init.main(folder=folder)
  elif ops[0] == 'config':
    from oiTerminal.cli import config
    logger: logging = getLogger(config_folder.get_file_path(OT_LOG))
    config.main(folder=folder, logger=logger)
  elif ops[0] == 'problem':
    from oiTerminal.cli import problem
    logger: logging = getLogger(config_folder.get_file_path(OT_LOG))
    problem.main(argv=args.args, logger=logger, folder=folder)
  elif ops[0] == 'contest':
    from oiTerminal.cli import contest
    logger: logging = getLogger(config_folder.get_file_path(OT_LOG))
    contest.main(argv=args.args, logger=logger, folder=folder)
  elif ops[0] == 'contestdetail':
    from oiTerminal.cli import contestdetail
    logger: logging = getLogger(config_folder.get_file_path(OT_LOG))
    contestdetail.main(argv=args.args, logger=logger, folder=folder)
  elif ops[0] == 'standing':
    from oiTerminal.cli import standing
    logger: logging = getLogger(config_folder.get_file_path(OT_LOG))
    standing.main(argv=args.args, logger=logger, folder=folder)
  # TODO
  #   reg
  #   web
  else:
    parser.print_help()


if __name__ == '__main__':
  main()

# DEBUG
# OITERMINAL_ENV=dev
