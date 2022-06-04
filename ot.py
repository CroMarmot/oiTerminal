#!/usr/bin/env python3
import argparse
import logging
from oiTerminal.cli.account import add_parser_account

from oiTerminal.cli.constant import OT_FOLDER, OT_LOG
from oiTerminal.cli.template import add_parser_template
from oiTerminal.utils.configFolder import ConfigFolder
from oiTerminal.utils.Logger import getLogger


def add_parser_config(parser_sub: argparse.ArgumentParser):
  # config
  parser_config = parser_sub.add_parser('config', help='template help')
  parser_config_sub = parser_config.add_subparsers(help='sub-command help')
  # account
  add_parser_account(parser_config_sub, func_prefix='config.')
  # template
  add_parser_template(parser_config_sub, func_prefix='config.')


def main():
  folder = OT_FOLDER
  config_folder = ConfigFolder(folder)
  parser = argparse.ArgumentParser(
      # prog='oi-cli',
      description='oiTerminal cli')
  parser_sub = parser.add_subparsers(help='sub-command help')

  # init
  parser_init = parser_sub.add_parser('init', help='init help')
  parser_init.set_defaults(func='init')
  # config
  add_parser_config(parser_sub)
  # TODO problem contest test submit

  # parse some argument lists
  # TODO move to auto test
  # args = parser.parse_args(['init'])
  # print(args)
  # print(args.func)

  # args = parser.parse_args(['config', 'account', 'list'])
  # print(args)
  # print(args.func)

  # args = parser.parse_args(['config', 'account', 'new', 'Codeforces', 'Cro-Marmot'])
  # print(args)
  # print(args.func)

  # args = parser.parse_args(['config', 'account', 'new', 'Codeforces', 'Cro-Marmot', '-d'])
  # print(args)
  # print(args.func)

  # args = parser.parse_args(['config', 'account', 'modify', 'Codeforces', 'Cro-Marmot', '-p'])
  # print(args)
  # print(args.func)

  # args = parser.parse_args(['config', 'account', 'delete', 'Codeforces', 'Cro-Marmot'])
  # print(args)
  # print(args.func)

  args = parser.parse_args()

  if args.func == 'init':
    from oiTerminal.cli import init
    init.main(folder=folder)
    return

  logger: logging = getLogger(config_folder.get_file_path(OT_LOG))
  logger.debug(f"args: {args} {args.func}")

  if args.func.startswith('config'):
    from oiTerminal.cli import config
    args.func = args.func[len('config.'):]
    config.main(folder=folder, logger=logger, args=args)

  exit(1)
  if ops[0] == 'problem':
    from oiTerminal.cli import problem
    problem.main(argv=args.args, logger=logger, folder=folder)
  elif ops[0] == 'contest':
    from oiTerminal.cli import contest
    contest.main(argv=args.args, logger=logger, folder=folder)
  elif ops[0] == 'contestlist':
    from oiTerminal.cli import contestlist
    contestlist.main(argv=args.args, logger=logger, folder=folder)
  elif ops[0] == 'contestdetail':
    from oiTerminal.cli import contestdetail
    contestdetail.main(argv=args.args, logger=logger, folder=folder)
  elif ops[0] == 'standing':
    from oiTerminal.cli import standing
    standing.main(argv=args.args, logger=logger, folder=folder)
  else:
    parser.print_help()


if __name__ == '__main__':
  main()
