#!/usr/bin/env python3
import os
import sys
from typing import List, Type

from oiTerminal.model.Analyze import Analyze
from oiTerminal.model.BaseOj import BaseOj
from oiTerminal.model.ParseProblemResult import ParseProblemResult
from oiTerminal.model.TestCase import TestCase

from oiTerminal.utils.FileUtil import FileUtil
from oiTerminal.utils.HtmlTag import HtmlTag
from oiTerminal.utils.HttpUtil import HttpUtil
from oiTerminal.utils.Logger import getLogger
from oiTerminal.utils.account import AccountManager
from oiTerminal.utils.configFolder import ConfigFolder
from oiTerminal.utils.consts.platforms import Platforms
from oiTerminal.utils.db import JsonFileDB

# file_util can be any thing , everything is file
from oiTerminal.utils.enc import AESCipher
from oiTerminal.utils.template import TemplateManager


def parse(oj: BaseOj, problem_id: str, file_util: Type[FileUtil], logger, template_manager, config_folder):
    template = template_manager.get_platform_default(type(oj).__name__)
    if template is None:
        print(type(oj).__name__ + ' has no default template, run ./oiTerminal.py config first')
        logger.warn(f'{type(oj).__name__} parse problem when no template set')
        return None

    result: ParseProblemResult = oj.problem(problem_id)
    test_cases: List[TestCase] = result.test_cases
    directory = config_folder.get_file_path(os.path.join('dist', type(oj).__name__, result.file_path))

    for i in range(len(test_cases)):
        file_util.write(config_folder.get_file_path(os.path.join(directory, f'in.{i}')), test_cases[i].in_data)
        file_util.write(config_folder.get_file_path(os.path.join(directory, f'out.{i}')), test_cases[i].out_data)

    # TODO switch directory
    # TODO 生成state.json ( 提供 自定义字段)
    file_util.copy(
        config_folder.get_file_path(template.path),
        config_folder.get_file_path(os.path.join(directory, os.path.basename(template.path)))
    )
    return directory


def main(argv: List[str], folder='.oiTerminal'):
    config_folder = ConfigFolder(folder)
    key = 'oiTerminal'
    user_config_path = config_folder.get_config_file_path('_userConfig.json')

    # TODO dynamic import
    logger = getLogger(config_folder.get_file_path('log/oiTerminal.log'))
    http_util = HttpUtil()
    template_manager = TemplateManager(
        JsonFileDB(
            file_path=user_config_path,
            logger=logger
        )
    )
    account_manager = AccountManager(
        db=JsonFileDB(
            file_path=user_config_path,
            logger=logger
        ),
        cipher=AESCipher(key)
    )

    if argv[0] == Platforms.codeforces:
        try:
            from oiTerminal.custom.Codeforces.Codeforces import Codeforces
            oj: BaseOj = Codeforces(
                http_util=http_util,
                logger=logger,
                account=account_manager.get_default_account(Codeforces.__name__),
                analyze=Analyze(),
                html_tag=HtmlTag(http_util)
            )
        except Exception as e:
            logger.exception(e)
            raise e
    else:
        raise Exception('Unknown Platform')

    directory = parse(
        oj=oj,
        problem_id=argv[1],
        file_util=FileUtil,
        logger=logger,
        template_manager=template_manager,
        config_folder=config_folder
    )

    if directory is None:
        return None
    print(directory)


if __name__ == '__main__':
    main(sys.argv)
