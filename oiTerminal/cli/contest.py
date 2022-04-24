#!/usr/bin/env python3
import json
import logging
import os
import sys
from typing import List, Type
from oiTerminal.cli.constant import CIPHER_KEY, OT_FOLDER, USER_CONFIG_FILE

from oiTerminal.model.Analyze import Analyze
from oiTerminal.model.BaseOj import BaseOj
from oiTerminal.model.FolderState import FolderState
from oiTerminal.model.ParseProblemResult import ParseProblemResult
from oiTerminal.model.TestCase import TestCase

from oiTerminal.utils.FileUtil import FileUtil
from oiTerminal.utils.HtmlTag import HtmlTag
from oiTerminal.utils.HttpUtil import HttpUtil
from oiTerminal.utils.account import AccountManager
from oiTerminal.utils.configFolder import ConfigFolder
from oiTerminal.utils.consts.platforms import Platforms
from oiTerminal.utils.db import JsonFileDB

# file_util can be any thing , everything is file
from oiTerminal.utils.enc import AESCipher
from oiTerminal.utils.force_symlink import force_symlink
from oiTerminal.utils.template import TemplateManager


def createDir(
    oj: BaseOj,
    contest_id: str,
    problem_ids: List[str],
    file_util: Type[FileUtil],
    logger,
    template_manager: TemplateManager,
    config_folder: ConfigFolder
):
  template = template_manager.get_platform_default(type(oj).__name__)
  if template is None:
    print(type(oj).__name__ +
          ' has no default template, run ./oiTerminal.py config first')
    logger.warn(f'{type(oj).__name__} parse problem when no template set')
    return None

  for v in problem_ids:
    problem_id = contest_id + v
    result: ParseProblemResult = oj.problem(problem_id)
    test_cases: List[TestCase] = result.test_cases
    directory = config_folder.get_file_path(
        os.path.join('dist', type(oj).__name__, contest_id, v))

    for i in range(len(test_cases)):
      file_util.write(config_folder.get_file_path(
          os.path.join(directory, f'in.{i}')), test_cases[i].in_data)
      file_util.write(config_folder.get_file_path(
          os.path.join(directory, f'out.{i}')), test_cases[i].out_data)

    # if code file exist not cover code
    if not os.path.exists(config_folder.get_file_path(os.path.join(
        directory, os.path.basename(template.path))
    )):
      file_util.copy(
          config_folder.get_file_path(template.path),
          config_folder.get_file_path(os.path.join(
              directory, os.path.basename(template.path)))
      )
    # TODO 生成state.json ( 提供 自定义字段)
    TEST_PY = 'test.py'
    SUBMIT_PY = 'submit.py'
    STATE_FILE = 'state.json'
    # symlink test.py submit.py
    RELATIVE_CLI_FOLDER = '../../../../'
    force_symlink(os.path.join(RELATIVE_CLI_FOLDER, TEST_PY),
                  config_folder.get_file_path(os.path.join(directory, TEST_PY)))
    force_symlink(os.path.join(RELATIVE_CLI_FOLDER, SUBMIT_PY),
                  config_folder.get_file_path(os.path.join(directory, SUBMIT_PY)))

    # TODO provide more info, like single test and
    # generate state.json
    folder_state = FolderState(
        oj=type(oj).__name__,
        sid=problem_id,
        template_alias=template.alias,
        lang='deperated',
        up_lang=54)  # TODO get data from analyzer
    with open(config_folder.get_file_path(os.path.join(directory, STATE_FILE)), "w") as statejson:
      json.dump(folder_state.__dict__, statejson)
      statejson.close()

  return config_folder.get_file_path(
        os.path.join('dist', type(oj).__name__, contest_id))


def main(argv: List[str], logger: logging, folder=OT_FOLDER):
  config_folder = ConfigFolder(folder)
  user_config_path = config_folder.get_config_file_path(USER_CONFIG_FILE)

  http_util = HttpUtil(logger=logger)
  dbIns = JsonFileDB(file_path=user_config_path, logger=logger)
  template_manager = TemplateManager(db=dbIns)
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

  problems = oj.get_problemids_in_contest(argv[1])
  problem_ids = list(map(lambda x: x['id'], problems))

  directory = createDir(
      oj=oj,
      contest_id=argv[1],
      problem_ids=problem_ids,
      file_util=FileUtil,
      logger=logger,
      template_manager=template_manager,
      config_folder=config_folder
  )
  print(directory)


if __name__ == '__main__':
  main(sys.argv, folder=OT_FOLDER)
