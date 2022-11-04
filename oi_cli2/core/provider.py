# simple IOC / DI
from typing import Any, Dict
from oi_cli2.core.DI import DI_ACCMAN, DI_CFG, DI_DB, DI_DB_COOKIES, DI_HTTP, DI_LOGGER, DI_PROVIDER, DI_TEMPMAN
from oi_cli2.cli.constant import CIPHER_KEY, COOKIES_FILE, OT_FOLDER, OT_LOG, USER_CONFIG_FILE
from oi_cli2.utils.HttpUtil import HttpUtil
from oi_cli2.utils.Logger import getLogger
from oi_cli2.utils.account import AccountManager
from oi_cli2.utils.configFolder import ConfigFolder
from oi_cli2.utils.db import JsonFileDB
from oi_cli2.utils.enc import AESCipher
from oi_cli2.utils.template import TemplateManager


class Provider:
  _objs: Dict[str, Any] = {}
  _fns: Dict[str, Any] = {}
  loop = 0  # 简单防止循环依赖

  def __init__(self) -> None:
    pass

  def reg(self, key: str, func) -> bool:
    assert key not in self._fns
    self._fns[key] = func
    return True

  def get(self, key: str):
    self.loop += 1
    assert key in self._fns
    assert (self.loop < 100)
    if key not in self._objs:
      self._objs[key] = self._fns[key]()

    self.loop -= 1
    return self._objs[key]


o = Provider()


def gen_cfg():
  return ConfigFolder(OT_FOLDER)


def gen_logger():
  try:
    config_folder: ConfigFolder = o.get(DI_CFG)
    logger = getLogger(config_folder.get_file_path(OT_LOG))
  except Exception as e:
    print(str(e))
    exit(1)
  return logger


def gen_template_manager():
  return TemplateManager(db=o.get(DI_DB))


def gen_account_manager():
  return AccountManager(db=o.get(DI_DB), cipher=AESCipher(CIPHER_KEY), logger=o.get(DI_LOGGER))


def gen_json_db():
  config_folder: ConfigFolder = o.get(DI_CFG)
  return JsonFileDB(config_folder.get_config_file_path(USER_CONFIG_FILE), logger=o.get(DI_LOGGER))


def gen_json_db_cookies():
  config_folder: ConfigFolder = o.get(DI_CFG)
  return JsonFileDB(config_folder.get_config_file_path(COOKIES_FILE), logger=o.get(DI_LOGGER))


def gen_http_util():
  return HttpUtil(logger=o.get(DI_LOGGER))


o.reg(DI_CFG, gen_cfg)
o.reg(DI_LOGGER, gen_logger)
o.reg(DI_HTTP, gen_http_util)
o.reg(DI_DB, gen_json_db)
o.reg(DI_DB_COOKIES, gen_json_db_cookies)
o.reg(DI_ACCMAN, gen_account_manager)
o.reg(DI_TEMPMAN, gen_template_manager)
