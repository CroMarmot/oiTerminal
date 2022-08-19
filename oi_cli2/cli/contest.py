#!/usr/bin/env python3
import asyncio
from enum import Enum
import json
import logging
import os
import threading
import time
from requests.exceptions import ReadTimeout, ConnectTimeout
from typing import List
from rich.live import Live
from rich.table import Table
import click
from rich.console import Console
from oi_cli2.core.DI import DI_ACCMAN, DI_CFG, DI_HTTP, DI_LOGGER, DI_TEMPMAN
import oi_cli2.core.provider as provider
from oi_cli2.custom.Codeforces.Codeforces import Codeforces

from oi_cli2.model.Analyze import Analyze
from oi_cli2.model.BaseOj import BaseOj
from oi_cli2.model.FolderState import FolderState
from oi_cli2.model.ParseProblemResult import ParseProblemResult
from oi_cli2.model.TestCase import TestCase

from oi_cli2.utils.FileUtil import FileUtil
from oi_cli2.utils.HtmlTag import HtmlTag
from oi_cli2.utils.HttpUtil import HttpUtil
from oi_cli2.utils.account import AccountManager
from oi_cli2.utils.configFolder import ConfigFolder
from oi_cli2.utils.consts.platforms import Platforms

# file_util can be any thing , everything is file
from oi_cli2.utils.template import TemplateManager

console = Console(color_system='256', style=None)


class VisitStatus(Enum):
  BEFORE = 1
  SUCCESS = 2
  FAILED = 3
  TIMEOUT = 3


visitedTextMap = {
    VisitStatus.BEFORE: "Fetching",
    VisitStatus.SUCCESS: "[green]OK",
    VisitStatus.FAILED: "[red]Failed",
    VisitStatus.TIMEOUT: "[red]Timeout",
}


def all_visit(result) -> Table:
  for v in result:
    if v[1] == VisitStatus.BEFORE:
      return False
  return True


def generate_table(result) -> Table:
  """Make a new table."""
  table = Table()
  table.add_column("Problem")
  table.add_column("Visited")
  table.add_column("Parse Status")

  for row in result:
    table.add_row(
        row[0],
        visitedTextMap[row[1]],
        "[green]OK" if row[2] else "Unknown",
    )
  return table


def createProblem(data, v, contest_id: str, template, oj: str):
  logger: logging.Logger = provider.o.get(DI_LOGGER)
  config_folder: ConfigFolder = provider.o.get(DI_CFG)
  timeOutRetry = 3
  while timeOutRetry >= 0:
    try:
      file_util = FileUtil
      problem_id = contest_id + v
      result: ParseProblemResult = oj.problem(problem_id)
      data[1] = VisitStatus.SUCCESS
      test_cases: List[TestCase] = result.test_cases
      directory = config_folder.get_file_path(os.path.join('dist', type(oj).__name__, contest_id, v))

      for i in range(len(test_cases)):
        file_util.write(config_folder.get_file_path(os.path.join(directory, f'in.{i}')), test_cases[i].in_data)
        file_util.write(config_folder.get_file_path(os.path.join(directory, f'out.{i}')), test_cases[i].out_data)

      # if code file exist not cover code
      if not os.path.exists(config_folder.get_file_path(os.path.join(directory, os.path.basename(template.path)))):
        file_util.copy(config_folder.get_file_path(template.path), config_folder.get_file_path(os.path.join(directory, os.path.basename(template.path))))
      # TODO 生成state.json ( 提供 自定义字段)
      STATE_FILE = 'state.json'

      # TODO provide more info, like single test and
      # generate state.json
      folder_state = FolderState(oj=type(oj).__name__, sid=problem_id, template_alias=template.alias, lang='deperated', up_lang=template.uplang)  # TODO get data from analyzer
      with open(config_folder.get_file_path(os.path.join(directory, STATE_FILE)), "w") as statejson:
        json.dump(folder_state.__dict__, statejson)
        statejson.close()
      data[2] = True
      return True
    except (ReadTimeout, ConnectTimeout) as e:
      logger.info(f'Http Timeout[{type(e).__name__}]: {e.request.url}')
      if timeOutRetry == 0:
        data[1] = VisitStatus.TIMEOUT
        return False
      timeOutRetry -= 1
      time.sleep(0.5)
    except Exception as e:
      logger.exception(type(e).__name__)
      logger.exception(e)
      data[1] = VisitStatus.FAILED
      return False


async def createDir(oj: BaseOj, contest_id: str, problem_ids: List[str]):
  logger: logging.Logger = provider.o.get(DI_LOGGER)
  config_folder: ConfigFolder = provider.o.get(DI_CFG)
  template_manager: TemplateManager = provider.o.get(DI_TEMPMAN)
  logger.debug(f"{oj},{contest_id},{problem_ids}")
  template = template_manager.get_platform_default(type(oj).__name__)
  if template is None:
    logger.error(type(oj).__name__ + ' has no default template, run `oi config` first')
    return None

  # ID, visited, success
  result = []
  for v in problem_ids:
    result.append([v, VisitStatus.BEFORE, False])

  tasks = []
  for i in range(len(problem_ids)):
    task = threading.Thread(target=createProblem, args=(result[i], problem_ids[i], contest_id, template, oj))
    tasks.append(task)
    task.start()

  with Live(generate_table(result), refresh_per_second=4) as live:
    while not all_visit(result):
      await asyncio.sleep(0.5)  # time.sleep 会卡住
      live.update(generate_table(result))

  for t in tasks:  # wait all task finished
    t.join()

  live.update(generate_table(result))

  return config_folder.get_file_path(os.path.join('dist', type(oj).__name__, contest_id))


@click.group()
def contest():
  """Contest relative(fetch,list,standing,detail)"""


@contest.command()
@click.argument('platform')
@click.argument('contestid')
def fetch(platform, contestid):
  """Fetch a contest(problems and testcases)

  PLATFORM    e.g. AtCoder, Codeforces

  CONTESTID   The id in the url, e.g. Codeforces(1122),AtCoder(abc230)
  """
  logger: logging.Logger = provider.o.get(DI_LOGGER)
  am: AccountManager = provider.o.get(DI_ACCMAN)
  http_util: HttpUtil = provider.o.get(DI_HTTP)

  if platform == Platforms.codeforces:
    try:
      from oi_cli2.custom.Codeforces.Codeforces import Codeforces
      oj: BaseOj = Codeforces(http_util=http_util, logger=logger, account=am.get_default_account(Codeforces.__name__), analyze=Analyze(), html_tag=HtmlTag(http_util))
    except Exception as e:
      logger.exception(e)
      raise e
  else:
    raise Exception('Unknown Platform')

  try:
    problems = oj.get_problemids_in_contest(contestid)
  except (ReadTimeout, ConnectTimeout) as e:
    logger.error(f'Http Timeout[{type(e).__name__}]: {e.request.url}')
    return
  except Exception as e:
    logger.exception(e)
    return

  logger.debug(f"{contestid},{problems}")
  problem_ids = list(map(lambda x: x['id'], problems))
  directory = asyncio.run(createDir(oj=oj, contest_id=contestid, problem_ids=problem_ids))
  console.print(f"[green bold] {directory} ")


@contest.command(name='list')
@click.argument('platform')
def list_command(platform: str):
  """list passed and recent contest

  PLATFORM    e.g. AtCoder, Codeforces
  """
  logger: logging.Logger = provider.o.get(DI_LOGGER)
  http_util: HttpUtil = provider.o.get(DI_HTTP)
  am: AccountManager = provider.o.get(DI_ACCMAN)

  if platform == Platforms.codeforces:
    try:
      from oi_cli2.custom.Codeforces.Codeforces import Codeforces
      oj: BaseOj = Codeforces(http_util=http_util, logger=logger, account=am.get_default_account(Codeforces.__name__), analyze=Analyze(), html_tag=HtmlTag(http_util))
    except Exception as e:
      logger.exception(e)
      raise e
  else:
    raise Exception('Unknown Platform')

  oj.print_contest_list()


@contest.command()
@click.argument('platform')
@click.argument('contestid')
def detail(platform, contestid):
  """Display problem set and your submit status of a specific contest"

  PLATFORM    e.g. AtCoder, Codeforces

  CONTESTID   The id in the url, e.g. Codeforces(1122),AtCoder(abc230)
  """
  logger: logging.Logger = provider.o.get(DI_LOGGER)
  http_util: HttpUtil = provider.o.get(DI_HTTP)
  am: AccountManager = provider.o.get(DI_ACCMAN)

  if platform == Platforms.codeforces:
    try:
      from oi_cli2.custom.Codeforces.Codeforces import Codeforces
      oj: BaseOj = Codeforces(http_util=http_util, logger=logger, account=am.get_default_account(Codeforces.__name__), analyze=Analyze(), html_tag=HtmlTag(http_util))
    except Exception as e:
      logger.exception(e)
      raise e
  else:
    raise Exception('Unknown Platform')

  oj.print_problems_in_contest(cid=contestid)


@contest.command()
@click.argument('platform')
@click.argument('contestid')
def standing(platform, contestid):
  """Display your friends standing of a specific contest"

  PLATFORM    e.g. AtCoder, Codeforces

  CONTESTID   The id in the url, e.g. Codeforces(1122),AtCoder(abc230)
  """
  logger: logging.Logger = provider.o.get(DI_LOGGER)
  http_util: HttpUtil = provider.o.get(DI_HTTP)
  am: AccountManager = provider.o.get(DI_ACCMAN)

  if platform == Platforms.codeforces:
    try:
      oj: BaseOj = Codeforces(http_util=http_util, logger=logger, account=am.get_default_account(Codeforces.__name__), analyze=Analyze(), html_tag=HtmlTag(http_util))
    except Exception as e:
      logger.exception(e)
      raise e
  else:
    raise Exception('Unknown Platform')

  oj.print_friends_standing(cid=contestid)
