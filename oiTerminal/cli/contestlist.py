#!/usr/bin/env python3
import logging
import sys
from typing import List 
from oiTerminal.cli.constant import CIPHER_KEY, OT_FOLDER, USER_CONFIG_FILE

from oiTerminal.model.Analyze import Analyze
from oiTerminal.model.BaseOj import BaseOj

from oiTerminal.utils.HtmlTag import HtmlTag
from oiTerminal.utils.HttpUtil import HttpUtil
from oiTerminal.utils.account import AccountManager
from oiTerminal.utils.configFolder import ConfigFolder
from oiTerminal.utils.consts.platforms import Platforms
from oiTerminal.utils.db import JsonFileDB

# file_util can be any thing , everything is file
from oiTerminal.utils.enc import AESCipher


def main(argv: List[str], logger: logging, folder=OT_FOLDER):
  config_folder = ConfigFolder(folder)
  user_config_path = config_folder.get_config_file_path(USER_CONFIG_FILE)

  http_util = HttpUtil(logger=logger)
  dbIns = JsonFileDB(file_path=user_config_path, logger=logger)
  account_manager = AccountManager(db=dbIns, cipher=AESCipher(CIPHER_KEY))

  if argv[0] == Platforms.codeforces:
    try:
      from oiTerminal.custom.Codeforces.Codeforces import Codeforces
      oj: BaseOj = Codeforces(
          http_util=http_util,
          logger=logger,
          account=account_manager.get_default_account(
              Codeforces.__name__),
          analyze=Analyze(),
          html_tag=HtmlTag(http_util)
      )
    except Exception as e:
      logger.exception(e)
      raise e
  else:
    raise Exception('Unknown Platform')

  oj.print_contest_list()


if __name__ == '__main__':
  main(sys.argv, folder=OT_FOLDER)
