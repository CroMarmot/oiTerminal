import logging
from typing import List
from oi_cli2.cli.adaptor.ojman import OJManager
from oi_cli2.cli.constant import CIPHER_KEY, OT_FOLDER, USER_CONFIG_FILE

from oi_cli2.model.BaseOj import BaseOj
from oi_cli2.utils.Provider2 import Provider2

from oi_cli2.utils.account import AccountManager
from oi_cli2.utils.configFolder import ConfigFolder
from oi_cli2.utils.db import JsonFileDB

# file_util can be any thing , everything is file
from oi_cli2.utils.enc import AESCipher


def main(argv: List[str], logger: logging.Logger, folder=OT_FOLDER):
  config_folder = ConfigFolder(folder)
  user_config_path = config_folder.get_config_file_path(USER_CONFIG_FILE)

  dbIns = JsonFileDB(file_path=user_config_path, logger=logger)
  account_manager = AccountManager(db=dbIns, cipher=AESCipher(CIPHER_KEY))

  platform = argv[0]
  try:
    oj: BaseOj = OJManager.createOj(platform=platform,
                                    account=account_manager.get_default_account(platform=platform),
                                    provider=Provider2())
  except Exception as e:
    logger.exception(e)
    raise e

  oj.print_friends_standing(cid=argv[1])


# if __name__ == '__main__':
#   main(sys.argv, folder=OT_FOLDER)
