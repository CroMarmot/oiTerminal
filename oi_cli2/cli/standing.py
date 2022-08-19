#!/usr/bin/env python3
import logging
import sys
from typing import List, Type
from oi_cli2.cli.constant import CIPHER_KEY, OT_FOLDER, USER_CONFIG_FILE

from oi_cli2.model.Analyze import Analyze
from oi_cli2.model.BaseOj import BaseOj

from oi_cli2.utils.HtmlTag import HtmlTag
from oi_cli2.utils.HttpUtil import HttpUtil
from oi_cli2.utils.OJUtil import OJUtil
from oi_cli2.utils.account import AccountManager
from oi_cli2.utils.configFolder import ConfigFolder
from oi_cli2.utils.db import JsonFileDB

# file_util can be any thing , everything is file
from oi_cli2.utils.enc import AESCipher


def main(argv: List[str], logger: logging, folder=OT_FOLDER):
  config_folder = ConfigFolder(folder)
  user_config_path = config_folder.get_config_file_path(USER_CONFIG_FILE)

  http_util = HttpUtil(logger=logger)
  dbIns = JsonFileDB(file_path=user_config_path, logger=logger)
  account_manager = AccountManager(db=dbIns, cipher=AESCipher(CIPHER_KEY))

  ojUtil = OJUtil()

  if argv[0] in ojUtil.short2class:
    oj_class: Type[BaseOj] = ojUtil.short2class[argv[0]]
    # oj_class.init(http_util=http_util, account_manager=account_manager, logger=logger)
    # oj_class.run(argv=argv[1:])
    try:
      oj: BaseOj = oj_class(
          http_util=http_util,
          logger=logger,
          account=account_manager.get_default_account(
              oj_class.__name__),
          analyze=Analyze(),
          html_tag=HtmlTag(http_util)
      )
    except Exception as e:
      logger.exception(e)
      raise e
  else:
    raise Exception('Unknown Platform')

  oj.print_friends_standing(cid=argv[1])


if __name__ == '__main__':
  main(sys.argv, folder=OT_FOLDER)