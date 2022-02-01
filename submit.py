#!/usr/bin/env python3
import json
from logging import getLogger
import logging
import time
import traceback
import os

from oiTerminal.cli.constant import CIPHER_KEY, GREEN, FETCH_RESULT_INTERVAL, STATE_FILE, DEFAULT, CONFIG_FILE, USER_CONFIG_FILE
from oiTerminal.cli.constant import OT_FOLDER, OT_LOG
from oiTerminal.model.Account import Account
from oiTerminal.model.Analyze import Analyze
from oiTerminal.model.BaseOj import BaseOj
from oiTerminal.utils import LanguageUtil
from oiTerminal.utils.HtmlTag import HtmlTag
from oiTerminal.utils.HttpUtil import HttpUtil

from oiTerminal.utils.account import AccountManager
from oiTerminal.model.FolderState import FolderState
from oiTerminal.model.Result import Result
from oiTerminal.utils.configFolder import ConfigFolder
from oiTerminal.utils.consts.platforms import Platforms
from oiTerminal.utils.db import JsonFileDB
from oiTerminal.utils.enc import AESCipher
from oiTerminal.utils.template import TemplateManager


def submit(
        core: BaseOj,
        pid: str,
        language: str,
        account: Account,
        file_path: str,
) -> Result:
  if not core.submit_code(pid=pid, language=language, code=file_path):
    raise Exception(f'submit failed,account={account.account}')
  print(f"{GREEN}Submitted{DEFAULT}")

  result = Result(Result.Status.PENDING)
  while result.cur_status in [Result.Status.RUNNING, Result.Status.PENDING]:
    print(f"Fetching result...({result.state_note})")
    time.sleep(FETCH_RESULT_INTERVAL)
    if result.quick_key != '':
      result = core.get_result_by_quick_id(result.quick_key)
    else:
      result = core.get_result(pid)
  return result


def submit_parser(root_folder: str, cipher: any):
  # get lang config
  if not os.path.isfile(STATE_FILE):
    raise Exception(f'STATE_FILE [{STATE_FILE}] NOT EXIST!')
  state_oj = FolderState()
  with open(STATE_FILE) as f:
    state_oj.__dict__ = json.load(f)

  oj = state_oj.oj
  up_lang = state_oj.up_lang

  dbIns = JsonFileDB(config_folder.get_config_file_path(USER_CONFIG_FILE), logger)
  account = AccountManager(db=dbIns, cipher=cipher).get_default_account(oj)
  template = TemplateManager(db=dbIns, platform=state_oj.oj).get_template_by_alias(state_oj.template_alias)

  if template is None:
    logging.error(f'Template not found by alias{state_oj.template_alias}')
    return False
  source_file_name = os.path.basename(template.path)
  code_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), source_file_name)
  if not os.path.isfile(code_file):
    raise Exception(f'code_file [{code_file}] NOT EXIST!')

  return oj, state_oj.id, up_lang, account, code_file


def submit_main(logger: logging, config_folder: ConfigFolder):
  ojname, pid, up_lang, account, code_path = submit_parser(
      root_folder=os.path.dirname(os.path.abspath(__file__)),
      cipher=AESCipher(CIPHER_KEY)
  )
  http_util = HttpUtil()
  if ojname == Platforms.codeforces:
    try:
      from oiTerminal.custom.Codeforces.Codeforces import Codeforces
      oj: BaseOj = Codeforces(
          http_util=http_util,
          logger=logger,
          account=account,
          analyze=Analyze(),
          html_tag=HtmlTag(http_util)
      )
    except Exception as e:
      logger.exception(e)
      raise e
  _result = submit(
      core=oj,
      pid=pid,
      language=up_lang,
      account=account,
      file_path=code_path,
  )
  print(f"SUBMIT[{_result.id}]:{_result.status_string}")
  print(f"{_result.time_note}|{_result.mem_note}")


if __name__ == '__main__':
  try:
    config_folder = ConfigFolder(OT_FOLDER)
    logger = getLogger(config_folder.get_file_path(OT_LOG))
    submit_main(logger=logger, config_folder=config_folder)
  except KeyboardInterrupt:
    logger.info("Interrupt by user")
  except Exception:
    logger.error(traceback.format_exc())
