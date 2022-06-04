#!/usr/bin/env python3
import argparse
from oiTerminal.cli.constant import USER_CONFIG_FILE
from oiTerminal.utils.configFolder import ConfigFolder
from oiTerminal.utils.db import JsonFileDB
import logging


def main(folder: str, logger: logging, args: argparse.Namespace):
  func = args.func
  print(func)
  config_folder = ConfigFolder(folder)
  db = JsonFileDB(config_folder.get_config_file_path(USER_CONFIG_FILE
                                                     ), logger=logger)
  if args.func.startswith('account'):
    args.func = args.func[len('account.'):]
    from oiTerminal.cli.account import account
    account(db, args=args, logger=logger)
  elif args.func.startswith('template'):
    args.func = args.func[len('template.'):]
    from oiTerminal.cli.template import template
    template(db, args=args)


if __name__ == '__main__':
  pass
