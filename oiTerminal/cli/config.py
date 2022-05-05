#!/usr/bin/env python3
from oiTerminal.cli.account import account
from oiTerminal.cli.analyze import analyze
from oiTerminal.cli.constant import OT_FOLDER, USER_CONFIG_FILE
from oiTerminal.cli.template import template
from oiTerminal.utils.configFolder import ConfigFolder
from oiTerminal.utils.db import JsonFileDB
import logging


def main(folder: str, logger: logging):
  while True:
    print("1) Account")
    print("2) Template")
    print("3) Analyze")
    try:
      index = int(input("> "))
    except Exception:
      print("input error")
      return

    config_folder = ConfigFolder(folder)
    db = JsonFileDB(config_folder.get_config_file_path(USER_CONFIG_FILE
                                                       ), logger=logger)

    if index == 1:
      account(db)
    elif index == 2:
      template(db)
    elif index == 3:
      analyze(db)
    else:
      print("input error")


if __name__ == '__main__':
  main(OT_FOLDER, logging)