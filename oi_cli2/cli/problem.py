#!/usr/bin/env python3
import logging
import os
import sys
import json
from typing import List, Type
from oi_cli2.cli.constant import CIPHER_KEY, OT_FOLDER, USER_CONFIG_FILE

from oi_cli2.model.BaseOj import BaseOj
from oi_cli2.model.ParseProblemResult import ParsedProblemResult
from oi_cli2.model.ProblemMeta import ProblemMeta
from oi_cli2.model.TestCase import TestCase
from oi_cli2.model.FolderState import FolderState

from oi_cli2.utils.FileUtil import FileUtil
from oi_cli2.utils.configFolder import ConfigFolder

# file_util can be any thing , everything is file
from oi_cli2.utils.template import TemplateManager
from oi_cli2.utils.force_symlink import force_symlink

# def createDir(oj: BaseOj, problem_id: str, problem: ProblemMeta, file_util: Type[FileUtil], logger,
#               template_manager: TemplateManager, config_folder: ConfigFolder):
#   template = template_manager.get_platform_default(type(oj).__name__)
#   if template is None:
#     print(type(oj).__name__ + ' has no default template, run ./oiTerminal.py config first')
#     logger.warn(f'{type(oj).__name__} parse problem when no template set')
#     return None
#
#   result = oj.problem(problem_id)
#   test_cases: List[TestCase] = result.test_cases
#   directory = config_folder.get_file_path(os.path.join('dist', type(oj).__name__, result.file_path))
#
#   for i in range(len(test_cases)):
#     file_util.write(config_folder.get_file_path(os.path.join(directory, f'in.{i}')), test_cases[i].in_data)
#     file_util.write(config_folder.get_file_path(os.path.join(directory, f'out.{i}')), test_cases[i].out_data)
#
#   # if code file exist not cover code
#   if not os.path.exists(config_folder.get_file_path(os.path.join(directory, os.path.basename(template.path)))):
#     file_util.copy(config_folder.get_file_path(template.path),
#                    config_folder.get_file_path(os.path.join(directory, os.path.basename(template.path))))
#   # TODO 生成state.json ( 提供 自定义字段)
#   TEST_PY = 'test.py'
#   SUBMIT_PY = 'submit.py'
#   STATE_FILE = 'state.json'
#   # symlink test.py submit.py
#   RELATIVE_CLI_FOLDER = '../../../../'
#   force_symlink(os.path.join(RELATIVE_CLI_FOLDER, TEST_PY),
#                 config_folder.get_file_path(os.path.join(directory, TEST_PY)))
#   force_symlink(os.path.join(RELATIVE_CLI_FOLDER, SUBMIT_PY),
#                 config_folder.get_file_path(os.path.join(directory, SUBMIT_PY)))
#
#   # TODO provide more info, like single test and
#   # generate state.json
#   folder_state = FolderState(oj=type(oj).__name__,
#                              sid=problem_id,
#                              template_alias=template.alias,
#                              up_lang=template.uplang)  # TODO get data from analyzer
#   with open(config_folder.get_file_path(os.path.join(directory, STATE_FILE)), "w") as statejson:
#     json.dump(folder_state.__dict__, statejson)
#     statejson.close()
#
#   return directory

# def main(argv: List[str], logger: logging, folder=OT_FOLDER):
#   config_folder = ConfigFolder(folder)
#   user_config_path = config_folder.get_config_file_path(USER_CONFIG_FILE)
#
#   http_util = HttpUtil(logger=logger)
#   dbIns = JsonFileDB(file_path=user_config_path, logger=logger)
#   template_manager = TemplateManager(db=dbIns)
#   account_manager = AccountManager(db=dbIns, cipher=AESCipher(CIPHER_KEY))
#
#   if argv[0] == Platforms.codeforces:
#     try:
#       from oi_cli2.custom.Codeforces.Codeforces import Codeforces
#       oj: BaseOj = Codeforces(http_util=http_util,
#                               logger=logger,
#                               account=account_manager.get_default_account(Codeforces.__name__),
#                               html_tag=HtmlTag(http_util))
#     except Exception as e:
#       logger.exception(e)
#       raise e
#   else:
#     raise Exception('Unknown Platform')
#
#   directory = createDir(
#       oj=oj,
#       problem_id=argv[1],
#       ProblemMeta=None,  # TODO support
#       file_util=FileUtil,
#       logger=logger,
#       template_manager=template_manager,
#       config_folder=config_folder)
#
#   if directory is None:
#     return None
#   # TODO switch directory
#   print(directory)
#
#   start_terminal(config_folder.get_file_path(os.path.join(directory)))

# if __name__ == '__main__':
#   main(sys.argv, folder=OT_FOLDER)
