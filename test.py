#!/usr/bin/env python3
import datetime
import json
import shutil
import traceback
import os
import logging
from types import FunctionType
from typing import List

from oiTerminal.cli.constant import OT_FOLDER, OT_LOG, ROOT_PATH, STATE_FILE, TEST_FOLDER, IN_SUFFIX, OUT_SUFFIX, GREEN, DEFAULT, USER_CONFIG_FILE
from oiTerminal.model.FolderState import FolderState
from oiTerminal.model.Template import Template
from oiTerminal.utils.configFolder import ConfigFolder
from oiTerminal.utils.Logger import getLogger
from oiTerminal.utils.db import JsonFileDB
from oiTerminal.utils.diffTool import diff_result
from oiTerminal.utils.template import TemplateManager


def tester(root_folder: str, test_files: List[str], testcase_folder: str, template: Template, diff_fn: FunctionType, logger: logging):
  # makefolder & mv code 2 folder
  os.makedirs(TEST_FOLDER, exist_ok=True)
  logger.info(f"test source files:{test_files}")
  for source_file_name in test_files:
    if not os.path.exists(source_file_name):
      raise FileNotFoundError(f"'{source_file_name}' not found!")
    shutil.copy(source_file_name, os.path.join(TEST_FOLDER, source_file_name))
  # compile
  os.chdir(TEST_FOLDER)
  if os.system(template.compilation) != 0:
    logger.error('Complete Failed.')
    return
  logger.debug('In Exist:'+os.path.join(root_folder, testcase_folder, f"{IN_SUFFIX}{0}"))

  # run  "" not better than 'time' in bash but worse is better :-)
  i = 0
  while os.path.isfile(os.path.join(root_folder, testcase_folder, f"{IN_SUFFIX}{i}")):
    std_in_file = os.path.join(root_folder, testcase_folder, f"{IN_SUFFIX}{i}")
    std_out_file = os.path.join(root_folder, testcase_folder, f"{OUT_SUFFIX}{i}")
    user_out_file = os.path.join(root_folder, TEST_FOLDER, f"{OUT_SUFFIX}{i}")
    start_time = datetime.datetime.now()
    logger.debug(f"{template.execute} < {std_in_file} > {user_out_file}")
    os.system(f"{template.execute} < {std_in_file} > {user_out_file}")
    end_time = datetime.datetime.now()
    print()
    # TODO COMPARE TIME
    print(f"TestCase {i} Time spend: {GREEN}{(end_time - start_time).total_seconds()}s{DEFAULT}")
    diff_fn(std_in_file, std_out_file, user_out_file)

    i += 1

  os.chdir("../")


def main(logger: logging, config_folder: ConfigFolder):
  logger.info(f"[test] start root path:{ROOT_PATH}")
  # get lang config
  if not os.path.isfile(STATE_FILE):
    raise Exception(f'STATE_FILE [{STATE_FILE}] NOT EXIST!')
  state_oj = FolderState()
  with open(STATE_FILE) as f:
    state_oj.__dict__ = json.load(f)

  dbIns = JsonFileDB(config_folder.get_config_file_path(USER_CONFIG_FILE), logger)
  template = TemplateManager(db=dbIns, platform=state_oj.oj).get_template_by_alias(state_oj.template_alias)

  if template is None:
    logging.error(f'Template not found by alias{state_oj.template_alias}')
    return False

  source_file_name = os.path.basename(template.path)
  tester(root_folder=os.path.dirname(os.path.abspath(__file__)), test_files=[
         source_file_name], testcase_folder='.', template=template, diff_fn=diff_result, logger=logger)

  # shutil.rmtree(TEST_FOLDER)
  logger.info('test finished')


if __name__ == '__main__':
  try:
    config_folder = ConfigFolder(OT_FOLDER)
    logger = getLogger(config_folder.get_file_path(OT_LOG))
    main(logger=logger, config_folder=config_folder)
  except KeyboardInterrupt:
    logger.info("Interrupt by user")
  except Exception as e:
    logger.error(traceback.format_exc())
