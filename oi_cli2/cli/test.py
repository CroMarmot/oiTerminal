#!/usr/bin/env python3
import datetime
import json
import logging
import os
import shutil
import traceback
from typing import List, Callable
import click
from rich.console import Console
from oi_cli2.cli.constant import DEFAULT, GREEN, IN_SUFFIX, OUT_SUFFIX, STATE_FILE, TEST_FOLDER
from oi_cli2.utils.Provider2 import Provider2
from oi_cli2.core.DI import DI_LOGGER, DI_TEMPMAN
from oi_cli2.model.FolderState import FolderState
from oi_cli2.model.Template import Template
from oi_cli2.utils.diffTool import diff_result_fn
from oi_cli2.utils.template import TemplateManager

console = Console(color_system='256', style=None)


def tester(root_folder: str, test_files: List[str], testcase_folder: str, template: Template,
           diff_fn: Callable[[str, str, str], None], logger: logging.Logger):
  # TODO, 这里似乎传入参数也是 abspath, 两个folder 似乎有点冗余, 还有test_folder
  logger.debug(f'{root_folder},{test_files},{testcase_folder}')
  # makefolder & mv code 2 folder
  os.makedirs(TEST_FOLDER, exist_ok=True)
  for source_file_name in test_files:
    if not os.path.exists(source_file_name):
      raise FileNotFoundError(f"'{source_file_name}' not found!")
    shutil.copy(source_file_name, os.path.join(TEST_FOLDER, source_file_name))
  # compile
  os.chdir(TEST_FOLDER)
  # TODO 非系统命令diff, 改为 自己实现函数/注入式/支持交互
  if os.system(template.compilation) != 0:
    logger.error('Complete Failed.')
    return

  logger.debug('In Exist:' + os.path.join(root_folder, testcase_folder, f"{IN_SUFFIX}{0}"))

  # run  "" not better than 'time' in bash but worse is better :-)
  i = 0
  while os.path.isfile(os.path.join(root_folder, testcase_folder, f"{IN_SUFFIX}{i}")):
    std_in_file = os.path.join(root_folder, testcase_folder, f"{IN_SUFFIX}{i}")
    std_out_file = os.path.join(root_folder, testcase_folder, f"{OUT_SUFFIX}{i}")
    user_out_file = os.path.join(root_folder, TEST_FOLDER, f"{OUT_SUFFIX}{i}")
    start_time = datetime.datetime.now()
    command = f'"{template.execute}" < "{std_in_file}" > "{user_out_file}"'
    logger.debug(command)
    os.system(command)
    end_time = datetime.datetime.now()
    print()
    # TODO COMPARE TIME
    print(f"TestCase {i} Time spend: {GREEN}{(end_time - start_time).total_seconds()}s{DEFAULT}")
    diff_fn(std_in_file, std_out_file, user_out_file)

    i += 1

  os.chdir("../")


def tst_main() -> bool:
  logger: logging.Logger = Provider2().get(DI_LOGGER)
  tm: TemplateManager = Provider2().get(DI_TEMPMAN)

  # get language config
  if not os.path.isfile(STATE_FILE):
    raise Exception(f'STATE_FILE [{STATE_FILE}] NOT EXIST!')
  state_oj = FolderState()
  with open(STATE_FILE) as f:
    state_oj.__dict__ = json.load(f)
  logger.debug(f'Loaded state:{state_oj}')

  template = tm.get_template_by_name(platform=state_oj.oj, name=state_oj.template_alias)

  if template is None:
    logger.error(f'Template not found by [{state_oj.oj},{state_oj.template_alias}]')
    return False

  source_file_name = os.path.basename(template.path)
  tester(root_folder=os.path.abspath('.'),
         test_files=[source_file_name],
         testcase_folder=os.path.abspath('.'),
         template=template,
         diff_fn=diff_result_fn,
         logger=logger)

  # shutil.rmtree(TEST_FOLDER)
  # logger.debug('test finished')
  return True


@click.command(name='test')
def tst_command() -> None:
  try:
    logger: logging.Logger = Provider2().get(DI_LOGGER)
    tst_main()
  except KeyboardInterrupt:
    logger.info("Interrupt by user")
  except Exception:
    logger.error(traceback.format_exc())
